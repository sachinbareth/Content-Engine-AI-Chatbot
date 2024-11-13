# src/document_processor.py
from typing import List
from pypdf import PdfReader
import os

class DocumentProcessor:
    def __init__(self, documents_path: str):
        """Initialize document processor with path to documents directory."""
        self.documents_path = documents_path
        
    def read_pdf(self, file_path: str) -> str:
        """Read a single PDF file and return its text content."""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF {file_path}: {str(e)}")
            return ""

    def process_documents(self) -> List[dict]:
        """Process all PDF documents in the documents directory."""
        documents = []
        for filename in os.listdir(self.documents_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(self.documents_path, filename)
                text = self.read_pdf(file_path)
                if text:
                    documents.append({
                        "content": text,
                        "metadata": {
                            "source": filename,
                            "type": "pdf"
                        }
                    })
        return documents

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size
            if end > text_length:
                end = text_length
            
            # Find the last period or newline in the chunk to avoid cutting sentences
            last_period = text[start:end].rfind('.')
            last_newline = text[start:end].rfind('\n')
            chunk_end = max(last_period, last_newline)
            
            if chunk_end == -1 or (end < text_length and chunk_end < chunk_size // 2):
                chunk_end = end
            else:
                chunk_end = start + chunk_end + 1
            
            chunks.append(text[start:chunk_end].strip())
            start = chunk_end - overlap
            
        return chunks