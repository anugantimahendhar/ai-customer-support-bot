import os
import streamlit as st

from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma


# ==================================================
# 1. Load .env
# ==================================================

load_dotenv()


# ==================================================
# 2. Get Google API Key
# ==================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# If .env does not have the key,
# get it from Streamlit Cloud Secrets
if not GOOGLE_API_KEY:
    GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")


# Check API key
if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is missing."
    )


# ==================================================
# 3. Create Vector Store
# ==================================================

def create_vectorstore():

    # Load policy files
    loader = DirectoryLoader(
        "data/policies",
        glob="*.txt",
        loader_cls=TextLoader
    )

    documents = loader.load()

    print(f"Loaded {len(documents)} policy files.")


    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(
        documents
    )

    print(f"Created {len(chunks)} chunks.")


    # Create Gemini embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY
    )


    # Create Chroma vector store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="vectorstore"
    )

    print("Vector store created successfully.")

    return vectorstore


# ==================================================
# 4. Test locally
# ==================================================

if __name__ == "__main__":

    vectorstore = create_vectorstore()

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )

    results = retriever.invoke(
        "How long do I have to return a product?"
    )

    print("\nRelevant policy information:\n")

    for result in results:

        print(result.page_content)
        print("-" * 50)