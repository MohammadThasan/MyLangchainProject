# Key Concepts You Learned
    # 🤖 LangChain
        # A framework that simplifies building applications with Large Language Models (LLMs)
    # Streamlit
        # A Python library to create web apps quickly without needing HTML/CSS/JavaScript
    #🦙 Ollama
        #A tool to run AI models locally on your computer without cloud services
    #📝 Prompt Templates
        # Reusable text structures with placeholders that get filled with user data

    # What Does This Code Do?
    # This Python code creates a Travel Guide Generator using AI. It combines LangChain (for AI interactions) and Streamlit (for the web interface).

# What Does This Code Do?
# This Python code creates a Travel Guide Generator using AI. It combines LangChain (for AI interactions) and Streamlit (for the web interface).

#-----------------------------------------#
# Step 1: Importing Dependencies
#-----------------------------------------#

# Explanation:
# os: A Python module for interacting with the operating system. In this code,
# it's imported but not actively used (it would be for getting environment variables).
# ChatOllama: From LangChain library - this is a wrapper for the Ollama chat model, which lets you run large language models (LLMs) locally on your computer.
# PromptTemplate: From LangChain - a tool to create reusable prompt structures with placeholders that you can fill in with different values.
# streamlit (st): A Python framework for creating interactive web applications quickly, especially for data science and AI demos.

import os
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
import streamlit as st

#-----------------------------------------#
# Step 2: Initializing the Language Model #
#-----------------------------------------#

# Explanation:
# This creates an instance of the ChatOllama model.
# model='gemma3:4b': Specifies which AI model to use - in this case, Gemma 3 with 4 billion parameters.
# The llm variable now holds your AI chatbot that you can ask questions and get responses from.
# Ollama allows you to run models locally without needing API keys or internet connectivity.

#OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
#OPENAI_API_KEY=""
llm=ChatOllama(model="gemma3:4b")

#------------------------------------#
# Step 3: Creating a Prompt Template #
#------------------------------------#

# PromptTemplate: Creates a reusable template with placeholders.
# input_variables: Declares which variables can be used (Note: there's a mismatch - the list says 'country' and 'no_of_paras' but the template uses 'city' and 'budget').
# template: The actual text with placeholders in curly braces like {city}, {month}, {language}, and {budget}.
# This template will be filled with user inputs to create a personalized prompt for the AI.
# ⚠️ Bug Alert: The input_variables don't match the template placeholders!

prompt_template= PromptTemplate(
    input_variables=["country","no_of_paras","language"],
    template ="""Welcome to the {city} travel guide!
    If you're visiting in {month}, here's what you can do:
    1. Must-visit attractions.
    2. Local cuisine you must try.
    3. Useful phrases in {language}.
    4. Tips for traveling on a {budget} budget.
    Enjoy your trip!
    """
    )

#-------------------------------------#
# Step 4: Building the User Interface #
#-------------------------------------#

#💡 Explanation:
# st.title(): Creates a large heading 'Travel App' at the top of the web page.
# st.text_input(): Creates text input boxes where users can type information.
# Each text input stores the user's answer in a variable (city, month, language).
# st.selectbox(): Creates a dropdown menu with predefined options (Low, Medium, High) for the budget.
# These are Streamlit widgets that automatically create interactive web elements without HTML/CSS!

st.title("Travel App")
city = st.text_input("Enter a city: ")
month = st.text_input("Enter the month: ")
language = st.text_input("Enter the language: ")
budget = st.selectbox("Travel Budget",["Low", "Medium", "High"])

# 🤖 LangChain
# A framework that simplifies building applications with Large Language Models (LLMs)

#️ Streamlit
# A Python library to create web apps quickly without needing HTML/CSS/JavaScript

#🦙 Ollama
#A tool to run AI models locally on your computer without cloud services

#📝 Prompt Templates
# Reusable text structures with placeholders that get filled with user data

if city and month and language and budget:
    response = llm.invoke(prompt_template.format(city=city,
                                                 month=month,
                                                 language=language,
                                                 budget=budget
                                                 ))
    st.write(response.content)
