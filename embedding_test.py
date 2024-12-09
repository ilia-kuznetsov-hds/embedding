import os
import openai
from PyPDF2 import PdfReader
import chromadb
from chromadb.utils import embedding_functions


openai.api_key = <your api key>

#PDF_PATH_SINGLE = r"C:\Users\User\Desktop\firearm_articles\2024 StatMod2 Assignment 3 Journal article TSA Australian firearm law.pdf"
PDF_PATH_FOLDER = r"C:\Users\kuzne\Desktop\embedding"
OUTPUT_PATH = r"C:\Users\kuzne\Desktop\embedding"

DATABASE_PATH = r"C:\Users\kuzne\Documents\Python_repo\01_embedding"


def convert_pdf_to_text(pdf_path, output_folder):
    # Load PDF
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Save as a text file
    base_name = os.path.basename(pdf_path).replace(".pdf", "")
    output_path = os.path.join(output_folder, f"{base_name}.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Converted {pdf_path} to {output_path}")



def convert_folder(folder_path, output_folder):
    for article in os.listdir(folder_path):
        if article.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, article) 
            convert_pdf_to_text(pdf_path, output_folder)



# Example usage

#convert_pdf_to_text(PDF_PATH, OUTPUT_PATH)

convert_folder(PDF_PATH_FOLDER, OUTPUT_PATH)


client = chromadb.PersistentClient(path=DATABASE_PATH)
#default_ef = embedding_functions.DefaultEmbeddingFunction()

# Create a collection for your documents 
collection = client.get_or_create_collection(name="articles") # embedding_function=default_ef


def load_documents(documents_path: str):
    texts = []
    for article in os.listdir(documents_path):
        if article.endswith(".txt"):
            with open(os.path.join(documents_path, article), "r", encoding="utf-8") as f:
                text = f.read()
                # Simple chunking: split by paragraph or by every 500 words
                chunks = text.split("\n")
                for chunk in chunks:
                    if chunk.strip():
                        texts.append(chunk.strip())
    return texts

docs = load_documents(OUTPUT_PATH)



client_ai = openai.OpenAI()


# Using OpenAI embeddings function
def get_embedding(text: str) -> list:
    response = client_ai.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

# Add documents to the collection with embeddings
for i, doc in enumerate(docs):
    embedding = get_embedding(doc)
    collection.add(
        documents=[doc],
        metadatas=[{"source": f"chunk_{i}"}],
        ids=[f"doc_{i}"],
        embeddings=[embedding]
    )






