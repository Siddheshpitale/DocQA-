import faiss
import numpy as np


class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, embeddings, metadatas):
        if len(embeddings) == 0:
            raise ValueError("No embeddings provided to VectorStore")

        self.index.add(np.array(embeddings, dtype="float32"))
        self.metadata.extend(metadatas)

    def search(self, query_embedding, top_n=20):
        top_n = min(top_n, len(self.metadata))

        distances, indices = self.index.search(
            np.array([query_embedding], dtype="float32"),
            top_n
        )

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue

            similarity = 1 / (1 + dist)

            results.append({
                "score": similarity,
                "text": self.metadata[idx]["text"],
                "metadata": self.metadata[idx]["metadata"]
            })

        return results
