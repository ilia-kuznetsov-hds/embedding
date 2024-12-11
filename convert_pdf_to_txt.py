import os
from PyPDF2 import PdfReader


PDF_PATH_FOLDER = r"C:\Users\kuzne\Desktop\embedding"
OUTPUT_PATH = r"C:\Users\kuzne\Desktop\embedding"



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
convert_folder(PDF_PATH_FOLDER, OUTPUT_PATH)
