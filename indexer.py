import os
from parser import parse_files

Supported_extensions = ('.py', '.java', '.js', '.go', '.rb', '.php')

def build_index(code_dir, db_collection, embedding_model):
    print(f"starting to index: {code_dir}")

    all_chunks = []
    all_metadatas = []
    all_ids = []
    file_count = 0

    for root, _, files in os.walk("example_go_project"):
        for file in files:
            if file.endswith(Supported_extensions):
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    file_count += 1

                    # the parser main function is called (a list of objects)
                    chunks = parse_files(file_path)

                    for chunk in chunks:
                        all_chunks.append(chunk["text"])
                        all_metadatas.append(chunk["metadata"]) 
                        chunk_id = f"{file_path}_{chunk["metadata"]["chunk_num"]}"
                        all_ids.append(chunk_id)

        if (all_chunks):
            print(f"Adding {len(all_chunks)} chunks from {file_count} files to the index...")

            # creating embeddings:
            prefixed_chunks = ["search_documents: " + chunk for chunk in all_chunks]
            print("\n Generating embeddings for: ", len(all_chunks), "Wait for a moment ...")
            all_embeddings = embedding_model.encode(prefixed_chunks, show_progress_bar = True).tolist()
            print("\n -- Embeddings generated --")

            batch_size = 1000
            for i in range(0, len(all_chunks), batch_size):
                db_collection.upsert(
                    embeddings = all_embeddings[i : i+batch_size],
                    documents = all_chunks[i : i+batch_size],
                    metadatas = all_metadatas[i : i+batch_size],
                    ids = all_ids[i: i+batch_size]
                )
            print("indexing complete ...")
        else:
            print("No chunks found to index.")