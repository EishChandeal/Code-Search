import os

def get_lang_from_ext(file_path):
    # The ones that are supported for now
    ext_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.java': 'java',
        '.go': 'go',
        '.rb': 'ruby',
        '.php': 'php'
    }
    _, ext = os.path.splitext(file_path)
    # can't find it? then defaults to plaintext
    return ext_map.get(ext, "plaintext")