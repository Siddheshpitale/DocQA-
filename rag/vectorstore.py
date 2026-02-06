import faiss
import numpy as np


class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, embeddings, metadatas):
        self.index.add(np.array(embeddings).astype("float32"))
        self.metadata.extend(metadatas)

    def search(self, query_embedding, top_n=20):
        distances, indices = self.index.search(
            np.array([query_embedding]).astype("float32"),
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
