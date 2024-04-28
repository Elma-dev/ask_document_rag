import asyncio
import os
from typing import Optional, Sequence
from pathlib import Path
import nest_asyncio
from llama_index.core.postprocessor import MetadataReplacementPostProcessor
from llama_index.core.schema import BaseNode

from utils.summarize import summarize_document

nest_asyncio.apply()

import streamlit as st
from llama_index.core import Document, VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.llms.ollama import Ollama
from llama_index.llms.cohere import Cohere
from llama_index.embeddings.cohere import CohereEmbedding
from utils.advanced_rag import sentence_window_retrieval


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
    return {"storage_contex": StorageContext.from_defaults(vector_store=pgVectorStore), "vector_store": pgVectorStore}


def to_vector_store_index(documents: [Document] = None,storageContext: Optional[str] = None,vector_store=None):
    if documents:
        return VectorStoreIndex.from_documents(documents=documents, storage_context=storageContext)
    return VectorStoreIndex.from_vector_store(vector_store=vector_store)


def define_global_settings(setting: str, value):
    if setting == "llm":
        Settings.llm = value
    elif setting == "embed_model":
        Settings.embed_model = value
    elif setting == "chunks_size":
        Settings.chunk_size = value
    elif setting == "sentence_window":
        Settings.node_parser = value


@st.cache_resource(show_spinner=False)
def query_engine_from_doc(documents: [str] = None):
    ''' load_documents if not loaded before '''
    if documents:
        doc = read_file_to_doc(documents)
    '''advanced rag with sentence window'''
    sentence_nodes = sentence_window_retrieval()
    '''create embedding'''
    # embed_mod = HuggingFaceEmbedding("sentence-transformers/all-mpnet-base-v2")
    cohere_embed = CohereEmbedding(cohere_api_key="2DNlMKIjntYyI9fflsvWJ9Nqn0cfZSyZUV92J2o6")
    '''create our llm mistral from ollama'''
    # llm = Ollama(model="mistral", base_url="https://b043-104-196-20-41.ngrok-free.app")
    cohere_llm = Cohere(api_key="2DNlMKIjntYyI9fflsvWJ9Nqn0cfZSyZUV92J2o6")
    '''set Settings'''
    define_global_settings("llm", cohere_llm)
    define_global_settings("embed_model", cohere_embed)
    define_global_settings("sentence_window", sentence_nodes)
    '''create storage context'''
    store_context, pg_vect = create_storage_context(db_name="rag_db", table="test_table2", embed_dim=1024).values()
    '''document to vector store'''
    vect_stor = to_vector_store_index(documents=[doc] if documents else None, storageContext=store_context,vector_store=pg_vect)
    postproc = MetadataReplacementPostProcessor(target_metadata_key="window")
    '''query engine'''
    return vect_stor.as_query_engine(similarity_top_k=2, node_postprocessors=[postproc])


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


def save_file(path:Path, file=None):
    with open(path, mode="wb") as f:
        f.write(file.getvalue())
    return path.exists()


if __name__ == '__main__':
    initialize_session_storage()
    container = st.container(height=430, border=True)
    with container:
        read_from_session_state()
    if file := st.file_uploader(" ", type="pdf"):
        path = Path("./files", file.name)
        if not path.exists():
            if save_file(path,file=file):
                query_engine = query_engine_from_doc([f"files/{file.name}"])
        else:
            query_engine=query_engine_from_doc()
    try:
        chat, summary = st.columns([0.86, 0.14])
        with chat:
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
        with summary:
            # user want to summarize the pdf file ..
            if st.button("summary"):
                summarize_document()
    except NameError:
        st.error(NameError)
        st.error("Please choose your file!", icon="😤")
