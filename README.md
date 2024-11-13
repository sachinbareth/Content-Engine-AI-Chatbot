# Content Engine AI Chatbot

Content Engine is a document analysis system using Retrieval Augmented Generation (RAG) to analyze and compare multiple PDF documents. It includes a chatbot interface built with Streamlit, allowing users to query and obtain insights from multiple documents simultaneously.

## 🌟 Features

- **PDF Document Processing**: Extracts and processes text from PDF files.
- **Local Embedding Generation**: Uses Sentence Transformers for generating embeddings.
- **Efficient Retrieval**: Uses ChromaDB for vector storage and efficient document retrieval.
- **Local Language Model**: Utilizes TinyLlama for generating natural language responses.
- **Interactive Chat Interface**: Streamlit-based chatbot for real-time querying.
- **Document Comparison & Analysis**: Compares and analyzes multiple documents side-by-side.
- **Fully Local Processing**: Operates entirely offline, with no external API dependencies.

## 🛠️ Technology Stack

- **Backend Framework**: r LangChain 
- **Frontend**: Streamlit
- **Vector Store**: ChromaDB (for efficient document retrieval and storage of embeddings)
- **Embedding Model**: Sentence Transformers (using `all-MiniLM-L6-v2`)
- **Language Model**: TinyLlama-1.1B-Chat
- **PDF Processing**: PyPDF (via `PdfReader` for PDF text extraction)
- **Environment Variables**: `dotenv` for configuration

## 📋 Prerequisites

- **Python**: Version 3.9 or higher
- **CUDA-capable GPU** (optional): For faster processing
- **Disk Space**: For document storage and vector embeddings

## 🚀 Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/sachinbareth/Content-Engine-AI-Chatbot.git
    cd content-engine
    ```

2. Run the setup script:

    ```bash
    python setup.py
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Place your PDF documents in the `data/documents` directory.

5. Run the application:

    ```bash
    streamlit run app.py
    ```

## 📁 Project Structure

```plaintext
content-engine/
│
├── src/
│   ├── document_processor.py      # Handles PDF reading and text extraction
│   ├── embeddings.py              # Generates and manages document embeddings
│   ├── llm.py                     # Local language model handler
│   ├── query_engine.py            # Orchestrates the query processing pipeline
│   └── vector_store.py            # Manages document storage and retrieval with ChromaDB
│
├── data/
│   ├── documents/                 # Directory for storing PDF files
│   └── chroma/                    # Directory for vector store persistence
│
├── app.py                         # Streamlit application
├── setup.py                       # Project setup script
├── requirements.txt               # Project dependencies
├── Dockerfile                     # Docker configuration
└── .env                           # Environment configuration
