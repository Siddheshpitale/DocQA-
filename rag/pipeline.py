import os
import pickle

from .loader import load_documents_from_folder
from .chunker import chunk_text
from .embedder import Embedder
from .vectorstore import VectorStore
from .retriever import dynamic_retrieve
from .qa import generate_answer


class RAGPipeline:
    def __init__(self, docs_path, max_pages=None):
        self.embedder = Embedder()

        # ✅ Unique cache per client/session
        client_id = os.path.basename(docs_path)
        cache_file = f"/tmp/vectorstore_{client_id}.pkl"

        if os.path.exists(cache_file):
            print("✅ Loading cached vector store...")
            with open(cache_file, "rb") as f:
                self.store = pickle.load(f)
            return

        print("⚠️ Building new vector store...")

        # ✅ Load documents with optional page limit
        documents = load_documents_from_folder(
            docs_path,
            max_pages=max_pages
        )

        if not documents:
            raise ValueError("No readable documents found.")

        chunks = chunk_text(documents)

        if not chunks:
            raise ValueError("Document chunking failed.")

        texts = [c["text"] for c in chunks]

        # ✅ SAFE batching → avoids RAM spike on Render
        self.store = None
        batch_size = 16

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_chunks = chunks[i:i + batch_size]

            batch_embeddings = self.embedder.embed(batch_texts)

            if self.store is None:
                self.store = VectorStore(dim=len(batch_embeddings[0]))

            self.store.add(batch_embeddings, batch_chunks)

        # ✅ Cache vector store (fast reload on next query)
        with open(cache_file, "wb") as f:
            pickle.dump(self.store, f)

        print("✅ Vector store cached successfully.")

    def ask(self, query):
        if not query:
            raise ValueError("Query cannot be empty.")

        if not hasattr(self, "store") or self.store is None:
            raise ValueError("Vector store not initialized.")

        query_embedding = self.embedder.embed([query])[0]
        raw_results = self.store.search(query_embedding)

        selected = dynamic_retrieve(raw_results)

        return generate_answer(query, selected)
