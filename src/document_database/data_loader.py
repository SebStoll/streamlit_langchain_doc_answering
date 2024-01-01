import streamlit as st

# used to load text
# from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import PyPDFLoader

# used to create the retriever
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings


# create the document database
@st.cache_resource(show_spinner=False)
def load_data(openai_api_key):
    with st.spinner(text="Loading and indexing the LLM blog – hang tight!."):
        loader = PyPDFLoader("data/raw/231231_wh40k_core_rules_10th_edition.pdf")
        data = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(data)
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        db = FAISS.from_documents(texts, embeddings)
        return db
