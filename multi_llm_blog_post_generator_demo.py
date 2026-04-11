# Why these prompts are great:
# You are a professional blogger": Giving the AI a "Persona" (Role prompting) instantly forces it to use a better, more conversational tone.
# Explicit Instructions: Telling it exactly what you want ("3 main points with subpoints") prevents the AI from hallucinating a massive,
    # 20-point list that ruins the layout of your blog.
# Chaining: Because Prompt 2 takes {outline} as its input, you guarantee that the Introduction paragraph perfectly matches the bullet points generated in Step 1.

import os
import streamlit as st
from langchain_community.chat_models import ChatOllama
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ==========================================
# SETUP: API Keys & AI Engines
# ==========================================
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("🚫 OpenAI API Key missing! Please set it in your environment.")
    st.stop()

# Initialize our two AI tools
llm1 = ChatOpenAI(model="gpt-5", api_key=api_key)
audio_client = OpenAI(api_key=api_key)

llm2 = ChatOllama(model="gemma3:4b")


# ==========================================
# STEP 1: Function to Generate the Outline
# ==========================================
def generate_outline(blog_topic, target_language):
    prompt = PromptTemplate.from_template("""
        You are a professional blogger. Create an outline for a blog post on: {topic}.
        The outline should Include: 
        - Introduction
        - 3 main points with subpoints
        - Conclusion.
        "IMPORTANT: The entire outline MUST be written in {language}."
    """)
    chain = prompt | llm1| StrOutputParser()
    return chain.invoke({
        "topic": blog_topic,
        "language": target_language
    })


# ==========================================
# STEP 2: Function to Generate the Introduction
# ==========================================
def generate_intro(blog_outline, blog_emotion, target_language):
    prompt = PromptTemplate.from_template("""
        You are a professional blogger. Write an engaging introduction paragraph.
        based on this outline: {outline}.
        The tone of the writing MUST be highly {emotion}.
        IMPORTANT: The introduction MUST be written in {language}.
        Hook the reader and overview the topic.
        Keep it concise, maximum 350 words.
    """)
    chain = prompt | llm2 | StrOutputParser()
    return chain.invoke({
        "outline": blog_outline,
        "emotion": blog_emotion,
        "language": target_language
    })


# ==========================================
# STEP 3: Function to Generate the Audio
# ==========================================
def generate_audio(text, chosen_voice):
    # Cut text at 4000 characters to prevent OpenAI crashes
    safe_text = text[:4000]

    # Note: OpenAI automatically detects the language and adjusts its accent!
    response = audio_client.audio.speech.create(
        model="tts-1",
        voice=chosen_voice,
        input=safe_text
    )
    return response.content


# ==========================================
# STEP 4: Build the User Interface (Streamlit)
# ==========================================
st.title("📝 Blog Post Generator")

# User Inputs
topic = st.text_input("1. Enter a blog topic:", placeholder="e.g., The Future of AI")

language = st.text_input("2. Enter Language:", placeholder="e.g., English, Spanish, French, Hindi")

emotions = [
    "Inspiring", "Passionate", "Empathetic", "Motivational",
    "Heartfelt", "Uplifting", "Empowering", "Sincere",
    "Hopeful", "Enthusiastic"
]
emotion = st.selectbox("3. Select Tone/Emotion:", emotions)

voice = st.selectbox("4. Select Audio Voice:", ["onyx", "echo", "fable", "alloy", "nova", "shimmer"])

# ==========================================
# STEP 5: Run the App (When Button is Clicked)
# ==========================================
if st.button("Generate Blog & Audio"):
    # Check if user filled in BOTH topic and language
    if not topic or not language:
        st.warning("⚠️ Please enter BOTH a topic and a language first.")
    else:
        try:
            with st.spinner(f"Writing and recording in {language}... please wait."):

                # Run the functions we built above!
                final_outline = generate_outline(topic, language)
                final_intro = generate_intro(final_outline, emotion, language)
                final_audio = generate_audio(final_intro, voice)

            # Display Outline
            st.subheader(f"📋 Blog Outline ({language})")
            st.write(final_outline)

            # Display Introduction
            st.subheader(f"✍️ Introduction ({emotion} Tone)")
            st.write(final_intro)

            # Display Audio Player
            st.subheader("🔊 Listen to Introduction")
            st.audio(final_audio, format="audio/mp3")

            # --- NEW: Download Button ---
            # Creates a clean file name by replacing spaces in the topic with underscores
            safe_filename = topic.replace(" ", "_") + "_intro.mp3"

            st.download_button(
                label="⬇️ Download Audio (MP3)",
                data=final_audio,
                file_name=safe_filename,
                mime="audio/mp3"
            )

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")