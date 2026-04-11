import os
from langchain_community.chat_models import ChatOllama

llm=ChatOllama(model="qwen3.5:4b")

question=input("what is the question?")
response = llm.invoke(question)
print(response)