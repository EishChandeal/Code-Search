from sentence_transformers import SentenceTransformer
# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("feature-extraction", model="microsoft/codebert-base")
# from transformers import AutoTokenizer, AutoModel
# import torch
# tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
# model = AutoModel.from_pretrained("microsoft/codebert-base")

print(pipe("def max(a,b): if a>b: return a else return b"))

print("Mic testing..")