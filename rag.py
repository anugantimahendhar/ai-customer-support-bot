import os
import streamlit as st

from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma


# ==================================================
# Load environment variables
# ==================================================

load_dotenv()


# ==================================================
# Get Google API Key
# ==================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# If running on Streamlit Cloud,
# get the key from Streamlit Secrets
if not GOOGLE_API_KEY:

    try:
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

    except Exception:
        GOOGLE_API_KEY = None


# ==================================================
# Validate API Key
# ==================================================

if not GOOGLE_API_KEY:

    raise ValueError(
        "GOOGLE_API_KEY is missing. "
        "Add it to your .env file locally "
        "or Streamlit Cloud Secrets."
    )


# ==================================================
# Create Vector Store
# ==================================================

def create_vectorstore():

    # ----------------------------------------------
    # Load policy documents
    # ----------------------------------------------

    loader = DirectoryLoader(
        "data/policies",
        glob="*.txt",
        loader_cls=TextLoader
    )

    documents = loader.load()

    print(
        f"Loaded {len(documents)} policy files."
    )


    # ----------------------------------------------
    # Split documents into chunks
    # ----------------------------------------------

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(
        documents
    )

    print(
        f"Created {len(chunks)} chunks."
    )


    # ----------------------------------------------
    # Create embeddings
    # ----------------------------------------------

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY
    )


    # ----------------------------------------------
    # Create Chroma vector store
    # ----------------------------------------------

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="vectorstore"
    )

    print(
        "Vector store created successfully."
    )

    return vectorstore


# ==================================================
# Test locally
# ==================================================

if __name__ == "__main__":

    vectorstore = create_vectorstore()


    # Create retriever

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )


    # Test retriever

    results = retriever.invoke(
        "How long do I have to return a product?"
    )


    print(
        "\nRelevant policy information:\n"
    )


    for result in results:

        print(result.page_content)

        print("-" * 50)