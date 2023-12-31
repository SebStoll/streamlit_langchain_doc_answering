import streamlit as st

# used to load text
# from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import PDFMinerLoader

# used to create the retriever
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings


# create the document database
@st.cache_resource(show_spinner=False)
def load_data(openai_api_key):
    with st.spinner(text="Loading and indexing the LLM blog – hang tight!."):
        # loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
        loader = PDFMinerLoader("data/raw/231231_wh40k_core_rules_10th_edition.pdf")
        data = loader.load()
        print (f'You have {len(data)} document(s) in your data')
        print (f'There are {len(data[0].page_content)} characters in your document')
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(data)
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        db = FAISS.from_documents(texts, embeddings)
        return db
