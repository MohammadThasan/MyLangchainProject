import os
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
# from langchain_openai import ChatOpenAI

# -------------------------------------------------------------------
# Initialize the local LLM (Qwen 3.5 4B via Ollama)
# Make sure you've pulled the model: ollama pull qwen3.5:4b
# -------------------------------------------------------------------
llm = ChatOllama(model="qwen3.5:4b")

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
