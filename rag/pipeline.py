import os
import pickle

from .loader import load_documents_from_folder
from .chunker import chunk_text
from .embedder import Embedder
from .vectorstore import VectorStore
from .retriever import dynamic_retrieve
from .qa import generate_answer


class RAGPipeline:
    def __init__(self, docs_path):
        self.embedder = Embedder()

        # ✅ Separate cache per uploaded document folder
        client_id = os.path.basename(docs_path)
        cache_file = f"/tmp/vectorstore_{client_id}.pkl"

        if os.path.exists(cache_file):
            print("✅ Loading cached vector store...")
            with open(cache_file, "rb") as f:
                self.store = pickle.load(f)
        else:
            print("⚠️ Building new vector store...")

            documents = load_documents_from_folder(docs_path)
            chunks = chunk_text(documents)

            texts = [c["text"] for c in chunks]

            # ✅ SAFE batching to prevent RAM spike
            self.store = None
            batch_size = 16

            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                batch_chunks = chunks[i:i + batch_size]

                batch_embeddings = self.embedder.embed(batch_texts)

                if self.store is None:
                    self.store = VectorStore(dim=len(batch_embeddings[0]))

                self.store.add(batch_embeddings, batch_chunks)

            # ✅ Cache vector store
            with open(cache_file, "wb") as f:
                pickle.dump(self.store, f)

            print("✅ Vector store cached successfully.")

    def ask(self, query):
        query_embedding = self.embedder.embed([query])[0]
        raw_results = self.store.search(query_embedding)
        selected = dynamic_retrieve(raw_results)
        return generate_answer(query, selected)
