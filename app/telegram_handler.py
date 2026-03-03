import re
from telegram import Update
from telegram.ext import ContextTypes
from app.session_manager import SessionManager
from app.transcript_service import (
    extract_video_id,
    fetch_transcript,
    TranscriptError,
)
from app.rag_engine import (
    chunk_transcript,
    build_faiss_index,
    retrieve_relevant_chunks,
)
from app.llm_service import ask_llama

session_manager = SessionManager()

YOUTUBE_REGEX = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"


# ----------------------------
# 1️⃣ Start Command
# ----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I help you analyze YouTube videos.\n\n"
        "📎 Send me a YouTube link to begin."
    )


# ----------------------------
# 2️⃣ Clear Session
# ----------------------------
async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session_manager.clear_session(user_id)

    await update.message.reply_text(
        "🔄 Session cleared successfully.\nSend a new YouTube link to start again."
    )


# ----------------------------
# 3️⃣ Main Message Handler
# ----------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    session = session_manager.get_session(user_id)

    # ============================
    # 🎥 CASE 1: YouTube Link
    # ============================
    if re.match(YOUTUBE_REGEX, text):
        try:
            session_manager.clear_session(user_id)
            session = session_manager.get_session(user_id)

            video_id = extract_video_id(text)

            await update.message.reply_text("📥 Fetching transcript...")

            transcript = fetch_transcript(video_id)
            chunks = chunk_transcript(transcript)

            if not chunks:
                await update.message.reply_text(
                    "❌ Could not process transcript properly."
                )
                return

            index, _ = build_faiss_index(chunks)

            session.video_id = video_id
            session.chunks = chunks
            session.index = index
            session.state = "VIDEO_READY"

            await update.message.reply_text(
                f"✅ Transcript loaded successfully!\n\n"
                f"🧱 Total chunks: {len(chunks)}\n"
                f"You can now ask questions about the video."
            )

        except TranscriptError as e:
            await update.message.reply_text(f"❌ {str(e)}")

        except Exception as e:
            print("Unexpected Error:", str(e))
            await update.message.reply_text(
                "❌ Something unexpected went wrong. Please try again."
            )

        return

    # ============================
    # 📎 CASE 2: No Video Loaded
    # ============================
    if session.state != "VIDEO_READY":
        await update.message.reply_text("📎 Please send a YouTube link first.")
        return

    # ============================
    # 🤖 CASE 3: Question Handling
    # ============================

    question = text.lower()

    # Step 1: Try normal retrieval
    if "seven" in question or "deadly" in question or "list" in question:
        relevant_chunks = retrieve_relevant_chunks(
            session.index,
            session.chunks,
            question,
            top_k=6   # Increase for list completeness
        )
    else:
        relevant_chunks = retrieve_relevant_chunks(
            session.index,
            session.chunks,
            question,
            top_k=3
        )

    # Step 2: If retrieval failed → fallback smartly
    if not relevant_chunks:
        relevant_chunks = session.chunks[:2]

    # Step 3: Ask LLM
    try:
        answer = ask_llama(relevant_chunks, question)
    except Exception as e:
        print("LLM Error:", str(e))
        await update.message.reply_text(
            "⚠️ Error generating response. Please try again."
        )
        return

    # Step 4: If LLM says not covered
    if "not covered" in answer.lower():
        await update.message.reply_text(answer)
        return

    # Step 5: Use first relevant chunk timestamp
    best_chunk = relevant_chunks[0]
    start_time = best_chunk["start"]

    timestamp_link = f"https://youtu.be/{session.video_id}?t={int(start_time)}"

    await update.message.reply_text(
        f"{answer}\n\n🔗 Jump to: {timestamp_link}"
    )