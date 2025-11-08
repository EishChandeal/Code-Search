import os
import chromadb
from sentence_transformers import SentenceTransformer
import indexer 
import shutil
import re

DB_PATH = "code_db"
COLLECTION_NAME = "code_search_test"
TEST_DIR = "example_go_project"

print("Started execution... \n\n")
print(f"Using test directory: {TEST_DIR}")
print(f"Using database path: {DB_PATH}")

dev_response = input("Want to remove previous db?: ")
if os.path.exists(DB_PATH):
    if re.match(r"^/?yes|^y$|sure|ok", dev_response, re.IGNORECASE):
        print("removing old vector database ..")
        shutil.rmtree(DB_PATH)
    else:
        pass

try:
    # This model is specifically for retrieval. `trust_remote_code=True` is required.
    model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)

    # est. connection with chroma
    client = chromadb.PersistentClient(path="code_db")

    # Use get_or_create_collection to avoid errors on subsequent runs
    collection = client.get_or_create_collection(
        name = COLLECTION_NAME
    )
    print("Starting off with indexing...")

    if not os.path.isdir(TEST_DIR):
        print("couldn't find the directory..")
    else:
        indexer.build_index(TEST_DIR, collection, model)
        print(f"total chunks in collection: {collection.count}")


    # test implementation of user natural language "search engine"
    user_query = "A funtion that gives greetings"
    print(f"Searching for: '{user_query}'")
    query_embedding = model.encode("search_query: " + user_query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include = ["documents","metadatas", "distances"]
    ) # can make the output more detailed look at docs

    print("\n> Search Results")
    if not results or not results["documents"][0]:   # understand the structure of output
        print("No results found")
    else:
        for i, per_query_result in enumerate(results["documents"]):  # multiple queries multiple sublists inside the main list: power of chroma i suppose
            print(f"\n--- Results for Query {i+1} ---")
            for j, code_chunk in enumerate(per_query_result):
                meta = results["metadatas"][i][j]
                dist = results["distances"][i][j]
                print(f"no.{j+1} \t Code chunk: \n {code_chunk}")
                print(f"distance: {dist}")
                print(f"meta_data: {meta}")
                print("\n")
                
except Exception as e:
    print(f"Error occured : {e}")

print("execution completed.")