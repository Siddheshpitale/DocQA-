def chunk_text(documents, chunk_size=300, overlap=40):
    chunks = []

    for doc in documents:
        text = doc["text"]
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]

            chunks.append({
                "text": chunk,
                "source": doc.get("source", "unknown")
            })

            start += chunk_size - overlap  # slide window

    print(f"✅ Created {len(chunks)} chunks")
    return chunks
