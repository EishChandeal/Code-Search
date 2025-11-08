import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
import indexer  
from utils import get_lang_from_ext 
import os

st.set_page_config(
    page_title = "Multilingual code search",
    layout = "centered"
)

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code= True)

@st.cache_resource
def get_db_collection():
    print("initializing chromadb")
    client = chromadb.Client()
    collection = client.get_or_create_collection(
        name = "code_search"
    )
    return collection

MODEL = load_embedding_model()
COLLECTION = get_db_collection()

st.title("++ Code Search ++")
st.markdown("Ask a question in natural language to search your code.")
st.sidebar.title("Controls")
st.sidebar.markdown("Add path to project folder.")

code_dir = st.sidebar.text_input(
    label="Enter the *full* path to your codebase:",   
    value = os.path.abspath("./test_codebase")
)