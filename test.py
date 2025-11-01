from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel
import torch

print("Started execution... \n\n")
snip = "def max(a,b): if a>b: return a else return b"

try:
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    model = AutoModel.from_pretrained("microsoft/codebert-base")

    # tokenized snippets
    code_tokens = tokenizer.tokenize(snip)

    # converted tokens into a numerical form
    code_token_ids = tokenizer.convert_tokens_to_ids(code_tokens)

    # Transformers expect their input to be in 2d form
    # These embeddings come from a giant lookup table (laymen) and ids are
    # positions from where definitions are fetched. 12 layers of attention
    # codebert has which makes highly contextualized embeddings
    context_embeddings=model(torch.tensor(code_token_ids)[None,:])[0]

    # Pooling. Replacing a 2d vector with one mean value.
    # Token dimensions and batch dimenstions to be kept in mind 
    # from [1, 17, 768] -> [1, 768], ([batch dim, token dim, semantic coordinates])
    mean_emd = torch.mean(context_embeddings, dim=1)
    print(mean_emd)
    
except Exception as e:
    print(f"Error occured: {e}")

print("execution complete!")