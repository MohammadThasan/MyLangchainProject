# ============================================
# STEP 1: Import all required libraries
# ============================================
import os
import io
import streamlit as st
from openai import OpenAI  # For Text-to-Speech
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# ============================================
# STEP 2: Load API Key
# ============================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("🚫 API Key not found!")
    st.stop()

# ============================================
# STEP 3: Create LLM + TTS Client
# ============================================
llm = ChatOpenAI(model="gpt-5", api_key=OPENAI_API_KEY)
tts_client = OpenAI(api_key=OPENAI_API_KEY)

# ============================================
# STEP 4: Create Prompt Templates
# ============================================
title_prompt = PromptTemplate(
    input_variables=["topic", "language"],
    template="""You are an experienced speech writer.
    Craft an impactful title for a speech about: {topic}
    Generate the title in {language}.
    Return ONLY the title, nothing else."""
)

speech_prompt = PromptTemplate(
    input_variables=["title", "language"],
    template="""Write a powerful speech of approximately 350 words 
    based on this title: {title}
    The speech must be in {language}."""
)

# ============================================
# STEP 5: Build LangChain Chains
# ============================================
title_chain = title_prompt | llm | StrOutputParser()
speech_chain = speech_prompt | llm | StrOutputParser()


# ============================================
# STEP 6: Text-to-Audio Function (OpenAI TTS)
# ============================================
def text_to_audio(text, voice="alloy"):
    """
    Converts text to human-like audio using OpenAI TTS.

    Available voices:
        onyx    → Deep male voice
        echo    → Warm male voice
        alloy   → Neutral voice
        fable   → Storytelling voice
        nova    → Friendly female voice
        shimmer → Soft female voice
    """
    response = tts_client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )

    audio_buffer = io.BytesIO()
    for chunk in response.iter_bytes():
        audio_buffer.write(chunk)
    audio_buffer.seek(0)
    return audio_buffer


# ============================================
# STEP 7: Streamlit UI
# ============================================
st.title("🎤 AI Speech Generator with Audio")

topic = st.text_input("📌 Enter a topic:", placeholder="e.g., Climate Change")
language = st.text_input("🌐 Enter a language:", placeholder="e.g., English")

voice = st.selectbox(
    "🎙️ Select Voice:",
    ["onyx", "echo", "alloy", "fable", "nova", "shimmer"],
    help="onyx/echo = Male | nova/shimmer = Female"
)

generate_btn = st.button("🚀 Generate Speech")

# ============================================
# STEP 8: Generate Speech + Audio on Click
# ============================================
if generate_btn:
    if not topic or not language:
        st.warning("⚠️ Please fill in all fields.")
    else:
        try:
            # Step A: Generate Title
            with st.spinner("Generating title..."):
                title = title_chain.invoke({
                    "topic": topic,
                    "language": language
                })
            st.subheader("🏆 Generated Title:")
            st.success(f"**{title}**")

            # Step B: Generate Speech
            with st.spinner("Writing speech..."):
                speech = speech_chain.invoke({
                    "title": title,
                    "language": language
                })
            st.subheader("📝 Full Speech:")
            st.markdown(speech)

            # Step C: Convert to Audio
            st.subheader("🔊 Listen to the Speech:")
            with st.spinner("Converting to audio..."):
                audio_bytes = text_to_audio(text=speech, voice=voice)

            st.audio(audio_bytes, format="audio/mp3")

            # Step D: Download Button
            st.download_button(
                label="⬇️ Download Audio (MP3)",
                data=audio_bytes,
                file_name=f"{topic}_speech.mp3",
                mime="audio/mp3"
            )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")