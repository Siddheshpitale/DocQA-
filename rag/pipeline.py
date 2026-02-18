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
        cache_file = "vectorstore.pkl"

        if os.path.exists(cache_file):
            print("✅ Loading cached vector store...")
            with open(cache_file, "rb") as f:
                self.store = pickle.load(f)
        else:
            print("⚠️ Building new vector store...")
            self.documents = load_documents_from_folder(docs_path)
            self.chunks = chunk_text(self.documents)

            texts = [c["text"] for c in self.chunks]
            embeddings = self.embedder.embed(texts)

            self.store = VectorStore(dim=len(embeddings[0]))
            self.store.add(embeddings, self.chunks)

            with open(cache_file, "wb") as f:
                pickle.dump(self.store, f)

            print("✅ Vector store cached successfully.")

    def ask(self, query):
        query_embedding = self.embedder.embed([query])[0]
        raw_results = self.store.search(query_embedding)
        selected = dynamic_retrieve(raw_results)
        return generate_answer(query, selected)
