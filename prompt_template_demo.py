import os
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# -------------------------------------------------------------------
# Choose your LLM backend:
# -------------------------------------------------------------------
# Option 1: Use OpenAI's API (requires a paid API key and setting OPENAI_API_KEY)
# from langchain_openai import ChatOpenAI
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

# Option 2: Use local Ollama (free, no API key needed)
# Make sure you have pulled the model: ollama pull qwen:4b
# from langchain_ollama import ChatOllama
# llm = ChatOllama(model="qwen:4b")

# Retrieve API key from local Environment variable in the system
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
#OPENAI_API_KEY=""
llm = ChatOpenAI(model = "gpt-4o-mini", api_key = OPENAI_API_KEY)

# -------------------------------------------------------------------
# Define the prompt template
# -------------------------------------------------------------------
prompt_template= PromptTemplate(
    input_variables=["country","no_of_paras","language"],
    template ="""You are an expert in traditional cuisines.
    You provide information about a specific dish from a specific country.
    Avoid giving information about fictional places. If the country is fictional
    or non-existent answer: I don't know.
    Answer the question: What is the traditional cuisine of {country}?
    Answer in {no_of_paras} and short paras in {language}?
    """
    )

# -------------------------------------------------------------------
# Streamlit UI
# -------------------------------------------------------------------
st.title("Cuisine App")
country = st.text_input("Enter a country: ")
no_of_paras = st.number_input("Enter the number of paragraphs: ",min_value=1,max_value=5, value=2)
language = st.text_input("Enter a Language (e.g., English, French): ")

if country:
    # Format the prompt with user inputs
    formatted_prompt = prompt_template.format(
        country=country,
        no_of_paras=no_of_paras,
        language=language
    )
    # Invoke the LLM
    response = llm.invoke(formatted_prompt)
    # Display the answer
    st.write(response.content)
