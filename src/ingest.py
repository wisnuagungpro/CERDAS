import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def ingest_pdfs():
    print("Ingesting PDF documents...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    pdf_dir = "data/pdfs_source"
    
    all_docs = []
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(pdf_dir, filename))
            all_docs.extend(loader.load())
            
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(all_docs)
    
    # Simpan ke ChromaDB
    Chroma.from_documents(docs, embeddings, persist_directory="./data/db")
    print(f"Successfully processed {len(docs)} chunks from PDFs.")

if __name__ == "__main__":
    ingest_pdfs()
