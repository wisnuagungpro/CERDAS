import os
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def ingest_documents():
    print("Ingesting documents...")
    # Load document
    loader = TextLoader("data/pdfs/panduan.txt")
    documents = loader.load()
    
    # Split document
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    
    # Embedding & Vector Store
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma.from_documents(docs, embeddings, persist_directory="./data/db")
    print(f"Ingested {len(docs)} documents into ChromaDB.")

if __name__ == "__main__":
    ingest_documents()
