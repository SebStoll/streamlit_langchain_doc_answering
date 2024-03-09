import sys
sys.path.append('C:\\projects\\streamlit_langchain_doc_answering')
import streamlit as st
from langchain.globals import set_debug, set_verbose
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

from src.document_database.data_loader import load_data

set_debug(True)
# set_verbose(True)

# set the secure key
openai_api_key = st.secrets.openai_key


# instantiate the database retriever
db = load_data(openai_api_key)
retriever = db.as_retriever()

# instantiate the large language model
llm = ChatOpenAI(temperature = 0, openai_api_key=openai_api_key)

qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        )


# add a heading for your app.
st.header("Chat with the Warhammer 40k core rule book (10th edition) 💬 📚")

if "history" not in st.session_state.keys():
    st.session_state['history'] = []

# Initialize the chat message history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about the Warhammer 40k core rules (10th edition)!"}
    ]


# Prompt for user input and display message history
if prompt := st.chat_input("Your Warhammer 40k core rules related question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Pass query to chat engine and display response
# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            #response = agent_executor({"input": prompt})
            response = qa_chain({"question": prompt, "chat_history": st.session_state['history']})
            st.write(response["answer"])
            message = {"role": "assistant", "content": response["answer"]}
            st.session_state.messages.append(message) # Add response to message history
            st.session_state['history'].append((prompt, response["answer"]))