from pypdf import PdfReader
from typing import List, Dict
import os


def load_pdf(file_path: str) -> List[Dict]:
    reader = PdfReader(file_path)
    documents = []

    for page_no, page in enumerate(reader.pages):
        text = page.extract_text()
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


def load_documents_from_folder(folder_path: str) -> List[Dict]:
    all_documents = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            all_documents.extend(load_pdf(file_path))

    return all_documents
