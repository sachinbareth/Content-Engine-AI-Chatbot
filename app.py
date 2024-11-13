# app.py
import streamlit as st
import os
from dotenv import load_dotenv
from src.document_processor import DocumentProcessor
from src.embeddings import EmbeddingsHandler
from src.vector_store import VectorStore
from src.llm import LLMHandler
from src.query_engine import QueryEngine

# Load environment variables
load_dotenv()

# Initialize components
@st.cache_resource
def initialize_components():
    # Initialize document processor
    doc_processor = DocumentProcessor("./data/documents")
    
    # Process documents if not already processed
    if not hasattr(st.session_state, 'documents_processed'):
        documents = doc_processor.process_documents()
        
        if documents:
            # Initialize embeddings handler
            embeddings_handler = EmbeddingsHandler()
            
            # Generate embeddings
            embeddings = embeddings_handler.generate_embeddings([doc["content"] for doc in documents])
            
            # Initialize vector store
            vector_store = VectorStore()
            
            # Add documents to vector store
            vector_store.add_documents(documents, embeddings)
            
            st.session_state.documents_processed = True
        else:
            st.error("No documents found in the data/documents directory!")
            st.stop()
    
    # Initialize LLM handler
    llm_handler = LLMHandler()
    
    # Initialize query engine
    query_engine = QueryEngine(
        embeddings_handler=embeddings_handler,
        vector_store=vector_store,
        llm_handler=llm_handler
    )
    
    return doc_processor, embeddings_handler, vector_store, query_engine

# Set up the Streamlit interface
st.title("Content Engine - Document Analysis")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Check for documents in the data directory
doc_dir = "./data/documents"
pdf_files = [f for f in os.listdir(doc_dir) if f.endswith('.pdf')] if os.path.exists(doc_dir) else []

if not pdf_files:
    st.error("No PDF files found! Please add PDF files to the data/documents directory.")
    st.stop()

# Initialize components
doc_processor, embeddings_handler, vector_store, query_engine = initialize_components()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about the documents"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = query_engine.process_query(prompt)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with document information
with st.sidebar:
    st.header("Document Information")
    st.write("Available Documents:")
    for filename in pdf_files:
        st.write(f"- {filename}")