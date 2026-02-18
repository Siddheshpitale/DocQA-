from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device="cpu"   # ✅ Force CPU
        )

    def embed(self, texts):
        return self.model.encode(
            texts,
            batch_size=32,                # ✅ Prevent RAM spikes
            show_progress_bar=False,
            convert_to_numpy=True,         # ✅ Needed for FAISS
            normalize_embeddings=True      # ✅ Better similarity search
        )
