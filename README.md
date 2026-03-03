🎥 YouTube Transcript RAG Telegram Bot

A Retrieval-Augmented Generation (RAG) powered Telegram bot that allows users to send a YouTube link, automatically fetch the transcript, and ask questions grounded strictly in the video content.

The bot uses semantic search (FAISS) and a locally served LLM (Llama 3.1 via Ollama) to provide context-aware answers along with direct timestamp links to the relevant part of the video.

🚀 Features

🔎 Semantic Retrieval with FAISS

1. Uses SentenceTransformers to create embeddings

2. Retrieves the most relevant transcript chunks

🧠 Local LLM Inference

1. Runs Llama 3.1 (8B) via Ollama

2. Fully local, private, and cost-free

🎯 Timestamp-Aware Answers

1. Each answer includes a clickable YouTube timestamp

❌ Hallucination Reduction

1. Similarity threshold filtering

2. Returns “This topic is not covered in the video.” when appropriate

🧩 Query-Aware Retrieval Strategy

1. Adapts chunk retrieval depth based on question intent

2. Uses structural retrieval for list-style queries

🔄 Sliding Window Chunking

1. Overlapping transcript chunks to improve recall quality

🏗 Architecture
User Message
↓
Telegram Bot (Async)
↓
Fetch YouTube Transcript
↓
Sliding Window Chunking (with overlap)
↓
Generate Embeddings (SentenceTransformers)
↓
FAISS Vector Index
↓
Retrieve Relevant Chunks
↓
LLM Answer Generation (Ollama - Llama 3.1)
↓
Return Answer + Timestamp Link

🛠 Tech Stack

1. Python

2. AsyncIO

3. python-telegram-bot

4. SentenceTransformers

5. FAISS (Vector Search)

6. Ollama (Local LLM Serving)

7. Llama 3.1 (8B)

8. YouTube Transcript API

⚙️ Setup Instructions

1️⃣ Clone the Repository

git clone https://github.com/yourusername/youtube-rag-telegram-bot.git
cd youtube-rag-telegram-bot

2️⃣ Create Virtual Environment

python -m venv .venv
.venv\Scripts\activate # Windows

# or

source .venv/bin/activate # Mac/Linux

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Configure Environment Variables

Copy .env.example to .env
TELEGRAM_BOT_TOKEN=your_token_here
OLLAMA_URL=http://127.0.0.1:11434/v1/chat/completions
MODEL_NAME=llama3.1:8b

5️⃣ Start Ollama

Make sure you have Ollama installed.

Pull the model:
ollama pull llama3.1:8b

Start the Ollama server:

ollama serve

6️⃣ Run the Bot

python -m app.main

You should see:
Bot is running...

📌 Example Usage
Send YouTube link
Ask:
“What is this video about?”
“What does he say about gossip?”
“Extract the seven deadly sins mentioned.”
“Who won the 2024 World Cup?”

If unrelated, the bot responds:
This topic is not covered in the video.

Each answer includes a timestamp link.

🧠 Key Design Decisions

Similarity Threshold Filtering
Reduces low-confidence retrieval results to prevent hallucinated answers.

Sliding Window Chunking
Improves semantic recall using overlapping transcript segments.

Query-Aware Retrieval
Adjusts retrieval strategy based on question type (enumeration vs conceptual).

Local LLM Serving
Avoids API costs and external dependencies by running Llama 3.1 locally via Ollama.

📊 What This Project Demonstrates

1. End-to-end RAG pipeline implementation

2. Vector search using FAISS

3. Semantic embedding generation

4. Local LLM integration

5. Async Telegram bot architecture

6. Context-grounded answer generation

7. Practical hallucination mitigation techniques

🔮 Future Improvements

1. Hybrid keyword + vector retrieval

2. Embedding caching for performance

3. Multi-video session memory

4. Web dashboard for monitoring

5. Dockerized deployment

📄 License
MIT License

🎯 Why This Project Matters

This project demonstrates the practical implementation of Retrieval-Augmented Generation using:

1. Real-world unstructured data (YouTube transcripts)

2. Semantic vector search

3. Local large language model inference

4. Context-grounded response generation

It reflects applied understanding of modern LLM system design beyond prompt engineering

## 🎬 Demo

Here is the bot in action:

![Demo](demo/demo.mp4)

### What the demo shows:
1. Sending YouTube link
2. Transcript loading
3. Asking question
4. Timestamp-based jump
5. Rejecting unrelated question