# src/vector_store.py
import chromadb
from chromadb.config import Settings
from typing import List, Dict
import os

class VectorStore:
    def __init__(self, persist_directory: str = "./data/chroma"):
        """Initialize the vector store."""
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                is_persistent=True
            )
        )
        
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, documents: List[Dict], embeddings: List[List[float]]):
        """Add documents and their embeddings to the vector store."""
        try:
            documents_data = []
            metadatas = []
            ids = []
            
            for i, doc in enumerate(documents):
                documents_data.append(doc["content"])
                metadatas.append(doc["metadata"])
                ids.append(f"doc_{i}")
            
            self.collection.add(
                embeddings=embeddings,
                documents=documents_data,
                metadatas=metadatas,
                ids=ids
            )
        except Exception as e:
            print(f"Error adding documents to vector store: {str(e)}")

    def query(self, query_embedding: List[float], n_results: int = 5) -> List[Dict]:
        """Query the vector store for similar documents."""
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            return [{
                "content": doc,
                "metadata": metadata,
                "distance": distance
            } for doc, metadata, distance in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )]
        except Exception as e:
            print(f"Error querying vector store: {str(e)}")
            return []