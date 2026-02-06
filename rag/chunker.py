def chunk_text(documents, chunk_size=400, overlap=50):
    chunks = []

    for doc in documents:
        text = doc["text"]
        metadata = doc["metadata"]

        words = text.split()
        start = 0
        chunk_id = 0

        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]

            chunks.append({
                "text": " ".join(chunk_words),
                "metadata": {
                    **metadata,
                    "chunk_id": chunk_id
                }
            })

            chunk_id += 1
            start += chunk_size - overlap

    return chunks
