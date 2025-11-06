import os 
import re 

DEFAULT_CHUNK_REGEX = r'\n\s*\n'

# can make language specific regex for now only did it for go
GO_CHUNK_REGEX = r'\n(?=func)'

# file_path = "example_go_project"

def parse_files(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file_path: {file_path} exiting with error: {e}")
        return []
    
    _, ext = os.path.splitext(file_path)
    if ext == (".go"):
        regex_pat = GO_CHUNK_REGEX
    else:
        regex_pat = DEFAULT_CHUNK_REGEX

    # breaking down the extracted content with regex function of our choice
    chunks = re.split(regex_pat, content)
    chunk_list = []

    for i, chunk_text in enumerate(chunks):
        cleaned_chunk = chunk_text.strip() # clean up whitespaces remove empty chunks
        if cleaned_chunk:
            chunk_list.append({
                "text" : cleaned_chunk,
                "metadata" : {
                    "file_path" : file_path,
                    "chunk_num" : i
                }
            })
    return chunk_list

if __name__ == "__main__":
    TEST_FILE_PATH = "example_go_project/newGo/todo.go" 
    if os.path.isfile(TEST_FILE_PATH):
        parsed_chunks = parse_files(TEST_FILE_PATH)

        for i, chunk in enumerate(parsed_chunks):
            print(f"\n--- CHUNK {i} ---")
            print(f"File: {chunk['metadata']['file_path']}")   # from within a dictionary containing dictionary
            print("--- Text ---")
            print(chunk['text'])
    else:
        print(f"Error: Test file not found at '{TEST_FILE_PATH}'")
        print(f"Please update the TEST_FILE_PATH variable in parser.py")