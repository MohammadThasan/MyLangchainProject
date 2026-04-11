import os
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.globals import set_debug

set_debug(True)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system","You are an Science coach, you can answer any questions related to Science subject. Dont answer any questions if they are not related to Science subject. If user asks such questions, just say, I dont know"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human","{input}")
    ]
)
chain = prompt_template | llm

history_for_chain = StreamlitChatMessageHistory()

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: history_for_chain,
    input_messages_key="input",
    history_messages_key="chat_history"
)

st.title("Science Coach")

input = st.text_input("Enter your question")

if input:
    response = chain_with_history.invoke({"input": input},
                                        {"configurable": {"session_id": "abc123"}}
                                         )
    st.write(response.content)

st.write("HISTORY")
st.write(history_for_chain)