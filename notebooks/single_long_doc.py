# used to load text
# from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import PyPDFLoader

# used to create the retriever
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings


# create the document database
def load_data(openai_api_key):
    loader = PyPDFLoader("../data/raw/231231_wh40k_core_rules_10th_edition.pdf")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    db = FAISS.from_documents(documents, embeddings)
    return db