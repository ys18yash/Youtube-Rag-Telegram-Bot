# app/rag_engine.py

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def chunk_transcript(transcript, chunk_size=500, overlap=100):
    chunks = []
    current_chunk = ""
    start_time = transcript[0]["start"]

    for segment in transcript:
        text = segment["text"]

        if len(current_chunk) + len(text) < chunk_size:
            current_chunk += " " + text
        else:
            chunks.append({
                "text": current_chunk.strip(),
                "start": start_time
            })
            start_time = segment["start"]
            current_chunk = current_chunk[-overlap:] + " " + text

    if current_chunk:
        chunks.append({
            "text": current_chunk.strip(),
            "start": start_time
        })

    return chunks


def build_faiss_index(chunks):
    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(texts, convert_to_numpy=True)

    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Inner Product = Cosine (after normalization)

    index.add(embeddings)

    return index, embeddings


import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_relevant_chunks(index, chunks, query, top_k=3):
    query_embedding = model.encode([query], convert_to_numpy=True)

    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:
        if idx < len(chunks):
            results.append(chunks[idx])

    return results