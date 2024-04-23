import asyncio
import os
from typing import Optional
from pathlib import Path
import nest_asyncio

nest_asyncio.apply()

import streamlit as st
from llama_index.core import Document, VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.llms.ollama import Ollama
from llama_index.llms.cohere import Cohere
from llama_index.embeddings.cohere import CohereEmbedding


# @st.cache_resource
def read_file_to_doc(fileNames: [str]):
    documents = SimpleDirectoryReader(input_files=fileNames).load_data()
    doc = Document(text="\\n".join([doc.text for doc in documents]))
    return doc


def create_storage_context(host: str = "localhost", port: str = "5432", username: str = "admin",
                           password: str = "admin", db_name: str = None, table: str = None, embed_dim: int = 1024):
    pgVectorStore = PGVectorStore.from_params(
        host=host,
        port=port,
        user=username,
        password=password,
        database=db_name,
        table_name=table,
        embed_dim=embed_dim
    )
    return StorageContext.from_defaults(vector_store=pgVectorStore)


def to_vector_store_index(documents: [Document], storageContext: Optional[str] = None):
    return VectorStoreIndex.from_documents(documents=documents, storage_context=storageContext)


def define_global_settings(setting: str, value: str):
    if setting == "llm":
        Settings.llm = value
    elif setting == "embed_model":
        Settings.embed_model = value
    elif setting=="chunks_size":
        Settings.chunk_size=value




@st.cache_resource(show_spinner=False)
def query_engine_from_doc(documents: [str]):
    # load_documents
    doc = read_file_to_doc(documents)
    # create embedding
        #embed_mod = HuggingFaceEmbedding("sentence-transformers/all-mpnet-base-v2")
    cohere_embed=CohereEmbedding(cohere_api_key="2DNlMKIjntYyI9fflsvWJ9Nqn0cfZSyZUV92J2o6")
    # create our llm mistral from ollama
     #   llm = Ollama(model="mistral", base_url="https://b043-104-196-20-41.ngrok-free.app")
    cohere_llm=Cohere(api_key="2DNlMKIjntYyI9fflsvWJ9Nqn0cfZSyZUV92J2o6")
    # set Settings
    define_global_settings("llm", cohere_llm)
    define_global_settings("embed_model", cohere_embed)
    # create storage context
    pgvectore_store_context = create_storage_context(db_name="rag_db", table="test_table2", embed_dim=1024)
    # document to vector store
    vect_stor = to_vector_store_index([doc], pgvectore_store_context)
    # query engine
    return vect_stor.as_query_engine()


# query_engine_from_doc(["files/my_resume.pdf"])

def initialize_session_storage():
    if "history" not in st.session_state:
        st.session_state.history = []


def read_from_session_state():
    for hist in st.session_state.history:
        with st.chat_message(hist["role"]):
            st.write(hist["query"])


def save_msg(role: str, message: str):
    st.session_state.history.append({"role": role, "query": message})


def save_file(where: str = "./files", file=None):
    path = Path(where, file.name)
    with open(path, mode="wb") as f:
        f.write(file.getvalue())
    return path.exists()


if __name__ == '__main__':
    initialize_session_storage()
    container = st.container(height=520, border=True)
    with container:
        read_from_session_state()
    if file := st.file_uploader("choose a file", type="pdf"):
        if save_file(file=file):
            query_engine = query_engine_from_doc([f"files/{file.name}"])
    try:
        if query := st.chat_input("ask document?"):
            with container:
                with st.chat_message("user"):
                    st.write(query)
                save_msg("user", query)
                with st.chat_message("assistant"):
                    with st.spinner(""):
                        response = query_engine.query(query).response
                        st.write(response)
                save_msg("assistant", response)
    except:
        st.error("Please choose your file!", icon="😤")
