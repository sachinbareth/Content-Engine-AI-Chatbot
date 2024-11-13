# src/query_engine.py
from typing import List, Dict
from .embeddings import EmbeddingsHandler
from .vector_store import VectorStore
from .llm import LLMHandler

class QueryEngine:
    def __init__(
        self,
        embeddings_handler: EmbeddingsHandler,
        vector_store: VectorStore,
        llm_handler: LLMHandler
    ):
        """Initialize the query engine with necessary components."""
        self.embeddings_handler = embeddings_handler
        self.vector_store = vector_store
        self.llm_handler = llm_handler

    def process_query(self, query: str, n_results: int = 5) -> str:
        """Process a query and generate a response."""
        try:
            # Generate embedding for the query
            query_embedding = self.embeddings_handler.generate_embeddings([query])[0]
            
            # Retrieve relevant documents
            relevant_docs = self.vector_store.query(
                query_embedding=query_embedding,
                n_results=n_results
            )
            
            # Generate response using LLM
            response = self.llm_handler.generate_response(query, relevant_docs)
            
            return response
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            return "I apologize, but I encountered an error while processing your query."