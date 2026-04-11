import os
from langchain_openai import ChatOpenAI
import prompt_template_demo as st

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
#OPENAI_API_KEY=""
llm=ChatOpenAI(model="gpt-4o-mini",api_key=OPENAI_API_KEY)

st.title("Ask any question from me")

question=st.text_input("what is the question?")
if question:
    response = llm.invoke(question)
    st.write(response.content)