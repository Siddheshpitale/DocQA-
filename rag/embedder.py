from sentence_transformers import SentenceTransformer

# ✅ Load ONCE at module level
model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device="cpu"
)

class Embedder:
    def embed(self, texts):
        return model.encode(
            texts,
            batch_size=32,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
