# Suppose user types: "Climate Change"
# title_prompt → creates prompt about creating a title
    # llm → generates: "Healing the Earth: Our Shared Duty"
    # StrOutputParser() → extracts that string
    # lambda title: ... →
    # Runs st.write("Healing the Earth: Our Shared Duty") → appears on screen
    # Returns "Healing the Earth: Our Shared Duty" → moves forward
    # That title goes into speech_prompt
    # second_chain → writes full speech based on the title

import os

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain_core.output_parsers import StrOutputParser

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
#OPENAI_API_KEY=""
llm=ChatOpenAI(model="gpt-4o-mini",api_key=OPENAI_API_KEY)
title_prompt= PromptTemplate(
    input_variables=["topic"],
    template ="""You are an experienced speech writer.
    You need to craft an impactful title for a speech
    on the following topic: {topic}
    Answer exactly with one title.
    """
    )

speech_prompt= PromptTemplate(
    input_variables=["title"],
    template ="""You need to write a powerful speech of 350 words
    for the following title: {title}
    """
    )
first_chain = title_prompt | llm | StrOutputParser() | (lambda title: (st.write(title),title)[1]) # Tuple
# This line builds a LangChain chain using the pipe operator |, which means:
# "Pass the output of one step as input to the next."
# Selects the second element (index 1) from the tuple.
# Result: Returns the title string, not None.
# This ensures the title continues flowing to the second_chain for speech generation.

second_chain = speech_prompt | llm

final_chain = first_chain | second_chain

st.title("Speech Generator")
topic = st.text_input("Enter a topic ")