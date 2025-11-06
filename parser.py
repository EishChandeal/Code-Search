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
    
    