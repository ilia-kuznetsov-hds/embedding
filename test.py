import os
import openai
from PyPDF2 import PdfReader
import chromadb
from chromadb.utils import embedding_functions


openai.api_key = <YOUR_API_KEY>

#PDF_PATH_SINGLE = r"C:\Users\User\Desktop\firearm_articles\2024 StatMod2 Assignment 3 Journal article TSA Australian firearm law.pdf"
PDF_PATH_FOLDER = r"C:\Users\kuzne\Desktop\embedding"
OUTPUT_PATH = r"C:\Users\kuzne\Desktop\embedding"

DATABASE_PATH = r"C:\Users\kuzne\Documents\Python_repo\01_embedding"


DOCUMENT_PATH = r"C:\Users\kuzne\Desktop\embedding\NEW_FILE.txt"

client = chromadb.PersistentClient(path=DATABASE_PATH)
#default_ef = embedding_functions.DefaultEmbeddingFunction()

# Create a collection for your documents 
collection = client.get_or_create_collection(name="articles") # embedding_function=default_ef


def load_documents(document_path: str):
    text = []
    with open(document_path, "r", encoding="utf-8") as f:
            text = f.read()
    return text

docs = load_documents(DOCUMENT_PATH)



client_ai = openai.OpenAI()


# Using OpenAI embeddings function
def get_embedding(text: str) -> list:
    response = client_ai.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

# Add documents to the collection with embeddings

embedding = get_embedding(docs)


print(embedding)
