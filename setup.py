from setuptools import setup, find_packages

setup(
    name="streamlit_langchain_doc_answering",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "openai",
        "streamlit",
    ],
)