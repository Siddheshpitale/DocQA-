# 📄 DocQA – Retrieval‑Augmented Document Question Answering

**Author:** Siddhesh Pitale

**GitHub:** [https://github.com/Siddheshpitale](https://github.com/Siddheshpitale)

**Repository:** [https://github.com/Siddheshpitale/DocQA-](https://github.com/Siddheshpitale/DocQA-)

---

## 🚀 Overview

**DocQA** is a Django‑based Document Question Answering system powered by a **Retrieval‑Augmented Generation (RAG)** pipeline. It allows users to upload PDF documents and ask natural‑language questions, returning **accurate, context‑aware answers with exact page‑level citations**.

This project is designed to be **modular, explainable, and hackathon‑ready**, with a clean separation between UI, backend orchestration, and the intelligence pipeline.

---

## ✨ Key Features

* 📤 Upload any PDF document
* 💬 Ask questions in natural language
* 🧠 RAG‑based answers grounded in document context
* 📌 Page‑level source attribution
* 🌗 Clean UI with Dark/Light mode
* ⚡ Modular pipeline (easy to extend or swap components)

---

## 🏗️ System Architecture

```
DocQA/
├── config/        # Django project configuration
├── frontend/     # UI, views, and request handling
├── rag/          # Core RAG intelligence pipeline
├── manage.py
├── db.sqlite3
└── .env
```

### 🔹 Frontend Layer (`frontend/`)

* Handles PDF upload and user queries
* Renders answers and citations
* Communicates with the RAG pipeline via Django views

### 🔹 RAG Pipeline (`rag/`)

* **loader.py** – PDF ingestion and text extraction
* **chunker.py** – Splits text into semantic chunks
* **embedder.py** – Converts text into embeddings
* **vectorstore.py / store.py** – Stores and manages vectors
* **retriever.py** – Semantic search over documents
* **qa.py** – Context‑aware answer generation
* **pipeline.py** – Orchestrates the full RAG workflow

---

## 🧠 How It Works

1. User uploads a PDF
2. Text is extracted and chunked
3. Chunks are embedded and stored in a vector database
4. User asks a question
5. Relevant chunks are retrieved via semantic search
6. An answer is generated using retrieved context
7. Source pages are displayed for transparency

---

## 🛠️ Tech Stack

* **Backend:** Django (Python)
* **AI Pipeline:** Retrieval‑Augmented Generation (RAG)
* **Embeddings:** Configurable (API/local models)
* **Vector Store:** Local / pluggable
* **Frontend:** HTML, CSS, JavaScript

---

## ⚙️ Setup & Installation

```bash
# Clone the repository
git clone https://github.com/Siddheshpitale/DocQA-
cd DocQA-

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add environment variables
# Create a .env file and add required API keys

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

Open: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🎯 Use Cases

* Academic document understanding
* Research paper Q&A
* Legal or policy document analysis
* Internal company documentation search

---

## 🏆 Why DocQA?

* Explainable AI with citations
* Clean, scalable architecture
* Production‑minded design
* Perfect for demos, hackathons, and extensions

---

## 📌 Future Enhancements

* Multiple document support
* Confidence scoring
* Answer summarization modes
* Vector DB swap (FAISS / Chroma)
* Deployment with Docker

---

## 📜 License

This project is open‑source and available under the **MIT License**.

---

⭐ If you find this project useful, consider giving it a star on GitHub!
