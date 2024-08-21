# Project Title: Ask Document RAG

## Overview

This project provides a sophisticated document retrieval system that leverages the capabilities of the LlamaIndex for efficient query processing. The architecture is designed to operate locally, integrating advanced Retrieval-Augmented Generation (RAG) strategies with powerful language models like Mistral, Gemma, and Meta for natural language processing.

## Architecture
![rag](https://github.com/Elma-dev/streamlit_llamaindex_rag/assets/67378945/9f58f788-692c-4acf-8e8c-568a5a0f5bb8)
The architecture is split into several key components:

1. **User Interface (UI)**
   - **Streamlit**: Provides a user-friendly interface for querying documents. Users interact with the system by entering their queries through the Streamlit application.

2. **Document Processing and Querying**
   - **Document Upload**: Users can upload documents which are then processed and stored locally.
   - **LlamaIndex**: 
     - **Chunking**: Documents are split into smaller, manageable chunks.
     - **Embedding**: Each chunk is embedded into a vector space using LlamaIndex’s vectorization techniques, allowing for efficient searching and retrieval.
     - **Advanced RAG Retrieval Strategies**: Implements advanced RAG strategies to enhance the retrieval process.
   - **Prompt Templates**: Custom templates are used to format and present the retrieved documents as context for generating responses.

3. **Data Storage**
   - **PostgreSQL**: A PostgreSQL database, running in a Docker container, is used to store the indexed chunks and their embeddings. This enables persistent storage and quick retrieval of document data.

4. **Language Model Interaction**
   - **Colab Machine**: A Google Colab instance is used to run the language models. This allows for powerful computation without requiring local resources.
   - **Ngrok**: Ngrok tunnels are used to securely expose the Colab machine's server to the local environment, facilitating communication between the components.
   - **Language Models**: Supports multiple models including Mistral AI, Gemma, and Meta, for generating responses based on the queries.

5. **Response Generation**
   - After retrieving the most relevant chunks from the database, the system formulates a prompt incorporating the retrieved context and sends it to the language model. The model then generates a response, which is relayed back to the user through the Streamlit interface.

## Setup and Installation

### Prerequisites

- Python 3.x
- Docker
- PostgreSQL
- Streamlit
- Google Colab Account
- Ngrok Account

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Elma-dev/ask_document_rag.git
   cd ask-document-rag```
2. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```
4. **Setup Ngrok for Colab Machine**
5. **Run the Application**
   ```
   streamlit run app.py
   ```
## Usage
**Upload Document:** Use the Streamlit interface to upload documents that you want to query.

**Submit Query:** Enter your query in the provided input box.

**Receive Response:** The system will process your query, retrieve the most relevant information from the documents, and generate a response using the language model. The response will be displayed on the Streamlit interface.
## Contributing
If you wish to contribute to this project, please fork the repository and submit a pull request with detailed information about the changes you made.


