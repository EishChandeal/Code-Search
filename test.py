from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel
import torch
import chromadb

print("Started execution... \n\n")
snips = ["def max(a,b): if a>b: return a else return b", 
         "function toCelsius(fahrenheit) {return (5/9) * (fahrenheit - 32);}",
         "func add(a, b int) int {return a + b}",
         "def greet(name):return f'Hello, {name}!'"]

try:
    # This model is specifically for retrieval. `trust_remote_code=True` is required.
    model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)

    # Nomic models work best if you add a "task prefix".
    prefixed_snips = ["search_document: " + snip for snip in snips]

    # both sentence_transformers and chromadb are optimized to work on batches
    print("Generating embeddings..")
    embeddings = model.encode(prefixed_snips)
    print(f"Generated {len(embeddings)} embeddings.")

    # just preparing example metadata that can be added into chromadb for testing:
    ids = [f"func_{i}" for i in range(len(snips))]
    metadatas = [{"File": f"func_{i}", "language": "python", "lines": 2} for i in range(len(snips))]

    # est. connection with chroma
    client = chromadb.PersistentClient(path="code_db")

    # Use get_or_create_collection to avoid errors on subsequent runs
    collection = client.get_or_create_collection("codebase_search")

    collection.upsert(
        ids = ids,
        embeddings = embeddings.tolist(),
        documents = snips,
        metadatas = metadatas
    )

    print("Snippets store in chromaDB.")


    # test implementation of user natural language "search engine"
    user_query = "a function that can tell me how hot I am feeling right now"
    print(f"Searching for: '{user_query}'")
    query_embedding = model.encode("search_query: " + user_query)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=2
    ) # can make the output more detailed look at docs

    print("\n--- Search Results ---")
    print(results)

        
except Exception as e:
    print(f"Error occured: {e}")

print("execution complete!")