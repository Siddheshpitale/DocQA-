from pypdf import PdfReader
from typing import List, Dict
import os


def load_pdf(file_path: str, max_pages=None) -> List[Dict]:
    reader = PdfReader(file_path)
    documents = []

    pages = reader.pages[:max_pages] if max_pages else reader.pages

    for page_no, page in enumerate(pages):
        try:
            text = page.extract_text()
        except Exception as e:
            print(f"⚠️ Failed to read page {page_no+1}: {e}")
            continue

        if text and text.strip():
            documents.append({
                "text": text.strip(),
                "metadata": {
                    "document": os.path.basename(file_path),
                    "source": file_path,
                    "page": page_no + 1
                }
            })

    return documents


def load_documents_from_folder(folder_path: str, max_pages=None) -> List[Dict]:
    all_documents = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)

            print(f"📄 Loading PDF: {filename}")

            docs = load_pdf(
                file_path,
                max_pages=max_pages
            )

            all_documents.extend(docs)

    if not all_documents:
        print("⚠️ No readable text found in PDFs.")

    return all_documents
