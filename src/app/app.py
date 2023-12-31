import sys
sys.path.append('C:\\projects\\streamlit_langchain_doc_answering')

import streamlit as st
import openai

from langchain.globals import set_debug, set_verbose
set_debug(True)
# set_verbose(True)

# used to create the memory
from langchain.memory import ConversationBufferMemory

# used to create the retrieval tool
# from langchain.agents import tool
from langchain.tools.retriever import create_retriever_tool

# used to create the prompt template
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema import SystemMessage
from langchain.prompts import MessagesPlaceholder


# used to create the agent executor
from langchain.chat_models import ChatOpenAI
# from langchain.agents import AgentExecutor
from langchain.agents import AgentExecutor, create_openai_tools_agent

from src.document_database.data_loader import load_data


# set the secure key
openai_api_key = st.secrets.openai_key

# add a heading for your app.
st.header("Chat with the LLM Agents blog 💬 📚")

# Initialize the memory
# This is needed for both the memory and the prompt
memory_key = "history"

if "memory" not in st.session_state.keys():
    st.session_state.memory = ConversationBufferMemory(memory_key=memory_key, return_messages=True)

# Initialize the chat message history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about LLM based agents!"}
    ]


db = load_data(openai_api_key)

# instantiate the database retriever
retriever = db.as_retriever()

# define the retriever tool
#@tool
#def tool(query):
#    """Searches and returns documents regarding Warhammer 40k core rules of the 10th edition"""
#    docs = retriever.get_relevant_documents(query)
#    return docs

tool = create_retriever_tool(
    retriever,
    "search_wh40k_rules",
    "Searches and returns excerpts from the Warhammer 40k (wh40k) core rule book (10th edition).",
)

tools = [tool]

# define the prompt
system_message = SystemMessage(
        content=(
            "You are a helpful assistant whose task is to answer questions on the Warhammer 40k (wh40k) core rule book (10th edition). "
            "Always try to answer the questions by using the tools provided. "
            "If you cannot answer the questions by using the tools provided, state so explicitly."
        )
)
prompt_template = OpenAIFunctionsAgent.create_prompt(
        system_message=system_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key)]
    )

# instantiate the large language model
llm = ChatOpenAI(temperature = 0, openai_api_key=openai_api_key)

# instantiate agent
# agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt_template)
agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=st.session_state.memory)

# Prompt for user input and display message history
if prompt := st.chat_input("Your LLM based agent related question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Pass query to chat engine and display response
# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = agent_executor({"input": prompt})
            st.write(response["output"])
            message = {"role": "assistant", "content": response["output"]}
            st.session_state.messages.append(message) # Add response to message history