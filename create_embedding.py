import os
import openai
import chromadb


openai.api_key = os.getenv("OPENAI_API_KEY")


PDF_PATH_FOLDER = r"C:\Users\kuzne\Desktop\embedding"
OUTPUT_PATH = r"C:\Users\kuzne\Desktop\embedding"

DATABASE_PATH = r"C:\Users\kuzne\Documents\Python_repo\01_embedding"

DOCUMENT_PATH = r"C:\Users\kuzne\Desktop\embedding\NEW_FILE.txt"

client = chromadb.PersistentClient(path=DATABASE_PATH)

# Create a collection for embeddings 
collection = client.get_or_create_collection(name="articles") 


def load_documents(document_path: str) -> str:
    text = []
    with open(document_path, "r", encoding="utf-8") as f:
        return f.read()

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
embedding = [embedding]



# Next task is to find out how to add the exctracted embedding into the database
#collection.add(
 #       documents= [docs],
 #       ids=[doc_id],
#        embeddings=[embedding]
 #   )