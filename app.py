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

if st.sidebar.button("Build index"):
    if not code_dir or not os.path.isdir(code_dir):
        st.sidebar.error(f"Error: Path '{code_dir}' is not a valid directory.")
    else:
        with st.sidebar:
            with st.spinner(f"indexing {code_dir}..."):
                indexer.build_index(code_dir, COLLECTION, MODEL)
            st.sidebar.success("indexing complete!")

# show the status of the database
st.sidebar.header("DB status")
db_count = COLLECTION.count()
st.sidebar.metric("Total code chunks:", db_count)

query = st.text_input("search query:" , placeholder= "program to greet the user")

if query:
    st.markdown("---")
    st.subheader("Search Results")

    with st.spinner("Searching..."):

        prefixed_query = "search_query: " + query

        query_embedding = MODEL.encode(prefixed_query).tolist()

        results = COLLECTION.query(
            query_embeddings= [query_embedding],
            n_results= 3
        )

        if not results["documents"][0]:
            st.warning("No result found.")
        else:
            for i, sub_doc in enumerate(results["documents"]):
                for j, per_query_doc in enumerate(sub_doc):
                    meta = results["metadatas"][i][j]
                    dist = results["distances"][i][j]
                    file_path = meta["file_path"]
                    lang = get_lang_from_ext(file_path)

                    with st.container(border= True):    
                        st.markdown(f"**File.** '{file_path}'")
                        st.markdown(f"**Relevance score: ** {dist:.4f} ")
                        st.markdown(f"**Rank: ** {j} **For query: ** {i}")
                        st.code(per_query_doc,language=lang)