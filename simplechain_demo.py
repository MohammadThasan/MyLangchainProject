# Import required libraries
import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain_core.output_parsers import StrOutputParser

# -----------------------------
# 1. Load API Key Securely
# -----------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if API key exists before running the app
if not OPENAI_API_KEY:
    st.error("🚫 Missing OpenAI API Key!")
    st.info("Set your key using: export OPENAI_API_KEY='your-key-here'")
    st.stop()  # Stop execution if key is missing

# Initialize the LLM model
llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

# -----------------------------
# 2. Define Prompt Templates
# -----------------------------
title_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""You are an experienced speech writer.
    You need to craft an impactful title for a speech
    on the following topic: {topic}
    Answer exactly with one title.
    """
)

speech_prompt = PromptTemplate(
    input_variables=["title"],
    template="""You need to write a powerful speech of 350 words
    for the following title: {title}
    """
)

# -----------------------------
# 3. Build LangChain Chains
# -----------------------------
# Chain 1: Generate Title
title_chain = title_prompt | llm | StrOutputParser()

# Chain 2: Generate Speech based on Title
speech_chain = speech_prompt | llm | StrOutputParser()

# -----------------------------
# 4. Create Streamlit UI
# -----------------------------
st.title("🎤 AI Speech Generator")
st.write("Enter a topic below to generate a speech title and full content.")

topic = st.text_input("Enter a topic:", placeholder="e.g., Climate Change")

# Add a button to trigger generation
generate_btn = st.button("Generate Speech")

# -----------------------------
# 5. Handle User Interaction
# -----------------------------
if generate_btn:

    # Validate input
    if not topic.strip():
        st.warning("⚠️ Please enter a valid topic.")

    else:
        try:
            # Show loading spinner while generating
            with st.spinner("Generating speech title..."):
                title = title_chain.invoke({"topic": topic})

            # Display the generated title clearly
            st.subheader("🏆 Generated Title:")
            st.markdown(f"**{title}**")

            with st.spinner("Writing speech content..."):
                speech = speech_chain.invoke({"title": title})

            # Display the full speech
            st.subheader("📝 Full Speech:")
            st.markdown(speech)

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")