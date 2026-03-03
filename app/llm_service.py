# app/llm_service.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL_NAME = os.getenv("MODEL_NAME")


def ask_llama(context_chunks, question):
    if not context_chunks:
        return "This topic is not covered in the video."

    context_text = "\n\n".join(chunk["text"][:800] for chunk in context_chunks)

    system_prompt = """
You are a precise assistant.

Answer ONLY using the provided transcript context.
Do NOT infer.
Do NOT add new concepts.
If the exact information is not explicitly present, say:
"This topic is not covered in the video."

When listing items, extract them exactly as written.
"""

    user_prompt = f"""
Transcript Context:
{context_text}

Question:
{question}
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print("LLM Error:", str(e))
        print(
            "Response Text:", response.text if "response" in locals() else "No response"
        )
        return "⚠️ Error generating response. Please try again."
