from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel
import torch

print("Started execution... \n\n")
snip = "def max(a,b): if a>b: return a else return b"

try:
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    model = AutoModel.from_pretrained("microsoft/codebert-base")

    code_tokens = tokenizer.tokenize(snip)
    code_token_ids = tokenizer.convert_tokens_to_ids(code_tokens)
    context_embeddings=model(torch.tensor(code_token_ids)[None,:])[0]

    print(context_embeddings)
except Exception as e:
    print(f"Error occured: {e}")

print("execution complete!")