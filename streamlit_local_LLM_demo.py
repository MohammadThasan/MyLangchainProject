import os
from langchain_community.chat_models import ChatOllama
import streamlit as st

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
#OPENAI_API_KEY=""
llm=ChatOllama(model="qwen3.5:4b")

st.title("Ask any question from me")

question=st.text_input("what is the question?")
if question:
    response = llm.invoke(question)
    st.write(response.content)

    llm = ChatOllama(model="qwen3.5:4b")

