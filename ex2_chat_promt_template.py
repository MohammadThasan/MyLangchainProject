import os
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system","You are an Science coach, you can answer any questions related to Science subject. Don't answer any questions if they are not related to Science subjects. If user asks such questions, just say 'I don't know'."),
        ("human","{input}")
    ]
)

st.title("Agile Coach")

input = st.text_input("Enter your question")

chain = prompt_template | llm

if input:
    response = chain.invoke({"input": input})
    st.write(response.content)