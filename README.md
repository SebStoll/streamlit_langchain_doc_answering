# Streamlit and Langchain Experiments Series: Document Question Answering
A Streamlit app which allows you to talk to a document of your choice. Per default you can ask questions to the Warhammer 40k 10th edition core rules.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)

## Installation
1. Ensure you have Python 3.11.4 or higher installed.
2. Clone this repository: `git clone https://github.com/SebStoll/streamlit_langchain_doc_answering.git`
3. Navigate to the project directory: `cd streamlit_langchain_doc_answering`
4. Install the dependencies: `pip install -r requirements.txt`
5. Get an OpenAI API key from https://platform.openai.com/.
6. Create folder `.streamlit` in the project root directory. In it, create a `secrets.toml` file and add your OpenAI secure key:
    ```
    openai_key = "<insert secure key here>"
    ```

## Usage
1. From the project root, run the Streamlit app: `streamlit run src/app/app.py`
2. The app should open in the browser. Follow the instructions there.
