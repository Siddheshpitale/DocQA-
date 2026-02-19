def chunk_text(documents, chunk_size=400, overlap=50):
    chunks = []

    for doc in documents:
        text = doc["text"]
        metadata = doc.get("metadata", {})  # ✅ Preserve metadata

        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]

            chunks.append({
                "text": chunk,
                "metadata": metadata   # ✅ CRITICAL FIX
            })

            start += chunk_size - overlap

    return chunks
