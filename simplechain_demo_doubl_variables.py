# Suppose user types: "Climate Change"
# title_prompt → creates prompt about creating a title
    # llm → generates: "Healing the Earth: Our Shared Duty"
    # StrOutputParser() → extracts that string
    # lambda title: ... →
    # Runs st.write("Healing the Earth: Our Shared Duty") → appears on screen
    # Returns "Healing the Earth: Our Shared Duty" → moves forward
    # That title goes into speech_prompt
    # second_chain → writes full speech based on the title

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
from langchain_core.globals import set_debug
#This is a very useful snippet! By running this code, you are enabling global debug mode in LangChain.
#Here is a breakdown of what it does, why it's useful, and an example of it in actio

set_debug(True) # It is not advisable to set the debug ON always
# What it does
# When you set set_debug(True), LangChain will print out everything happening under the hood to your console. This includes:

# The exact, formatted prompts being sent to the LLM.
# The exact parameters being passed to the LLM (temperature, max tokens, etc.).
# The raw JSON/API response received from the model.
# The exact inputs and outputs of every tool, chain, or agent step.
# Token usage statistics.

# -----------------------------
# 1. Load API Key Securely
# -----------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("🚫 OpenAI API Key not found!")
    st.stop()

llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

# -----------------------------
# 2. Define Prompt Templates
# -----------------------------
title_prompt = PromptTemplate(
    input_variables=["topic", "language"],
    template="""You are an experienced speech writer.
    Craft an impactful title for a speech about this topic: {topic}
    Generate the title in {language}.
    Return ONLY the title, nothing else."""
)

speech_prompt = PromptTemplate(
    input_variables=["title", "language"],
    template="""Write a powerful speech of approximately 350 words 
    based on this title: {title}
    The speech must be in {language}."""
)

# -----------------------------
# 3. Build Chains (Keep Pure - No UI Here)
# -----------------------------
title_chain = title_prompt | llm | StrOutputParser()
speech_chain = speech_prompt | llm | StrOutputParser()

# -----------------------------
# 4. Create Streamlit UI
# -----------------------------
st.title("🎤 AI Speech Generator")

topic = st.text_input("Enter a topic:", placeholder="e.g., Climate Change")
language = st.text_input("Enter a language:", placeholder="e.g., English")

generate_btn = st.button("Generate Speech")

# -----------------------------
# 5. Handle User Interaction
# -----------------------------
if generate_btn:
    if not topic or not language:
        st.warning("⚠️ Please fill in all fields.")
    else:
        try:
            with st.spinner("Generating title..."):
                title = title_chain.invoke({"topic": topic, "language": language})

            st.subheader("🏆 Generated Title:")
            st.markdown(f"**{title}**")

            with st.spinner("Writing speech content..."):
                speech = speech_chain.invoke({"title": title, "language": language})

            st.subheader("📝 Full Speech:")
            st.markdown(speech)

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")