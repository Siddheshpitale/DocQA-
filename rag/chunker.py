def chunk_text(documents, chunk_size=400, overlap=50):
    chunks = []
    chunk_id = 0   # ✅ ADD THIS

    for doc in documents:
        text = doc["text"]
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            if chunk_text.strip():
                chunks.append({
                    "text": chunk_text,
                    "metadata": doc["metadata"],
                    "chunk_id": chunk_id   # ✅ CRITICAL FIX
                })
                chunk_id += 1

            start += chunk_size - overlap

    return chunks
