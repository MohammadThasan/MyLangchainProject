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
import io
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from gtts import gTTS

# -----------------------------
# 1. Load API Key Securely
# -----------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("🚫 OpenAI API Key not found! Set OPENAI_API_KEY environment variable.")
    st.stop()

# -----------------------------
# 2. Initialize LLM
# -----------------------------
llm = ChatOpenAI(model="gpt-5", api_key=OPENAI_API_KEY)

# -----------------------------
# 3. Define Prompt Templates
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
# 4. Build Chains
# -----------------------------
title_chain = title_prompt | llm | StrOutputParser()
speech_chain = speech_prompt | llm | StrOutputParser()

# -----------------------------
# 5. Language Code Mapping
# -----------------------------
LANGUAGE_MAP = {
    "english": "en",
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "hindi": "hi",
    "urdu": "ur",
    "arabic": "ar",
    "chinese": "zh",
    "japanese": "ja",
    "portuguese": "pt",
    "italian": "it",
    "korean": "ko",
    "russian": "ru",
    "turkish": "tr",
    "dutch": "nl",
    "bengali": "bn",
    "tamil": "ta",
    "telugu": "te",
    "marathi": "mr",
    "gujarati": "gu",
}

# -----------------------------
# 6. Text to Audio Function
# -----------------------------
def text_to_audio(text, language_code="en"):
    """
    Converts text to audio using Google Text-to-Speech (gTTS).
    Returns audio as BytesIO object.
    """
    try:
        tts = gTTS(text=text, lang=language_code, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer
    except Exception as e:
        st.error(f"Audio conversion error: {str(e)}")
        return None

# -----------------------------
# 7. Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="AI Speech Generator",
    page_icon="🎤",
    layout="centered"
)

st.title("🎤 AI Speech Generator with Audio")
st.markdown("Generate a powerful speech on any topic and listen to it!")
st.markdown("---")

# Input Fields
topic = st.text_input(
    "📌 Enter a Topic:",
    placeholder="e.g., Climate Change, Education, Technology"
)

language = st.text_input(
    "🌐 Enter a Language:",
    placeholder="e.g., English, Hindi, Spanish, Urdu"
)

# Show supported languages
with st.expander("📋 Supported Languages for Audio"):
    supported = ", ".join([lang.title() for lang in LANGUAGE_MAP.keys()])
    st.write(supported)

generate_btn = st.button("🚀 Generate Speech", use_container_width=True)

# -----------------------------
# 8. Handle Generation
# -----------------------------
if generate_btn:
    if not topic or not language:
        st.warning("⚠️ Please fill in both Topic and Language fields.")
    else:
        try:
            # --- Step 1: Generate Title ---
            with st.spinner("✍️ Generating title..."):
                title = title_chain.invoke({
                    "topic": topic,
                    "language": language
                })

            st.subheader("🏆 Generated Title:")
            st.success(f"**{title}**")

            # --- Step 2: Generate Speech ---
            with st.spinner("📝 Writing speech content..."):
                speech = speech_chain.invoke({
                    "title": title,
                    "language": language
                })

            st.subheader("📝 Full Speech:")
            st.markdown(speech)

            st.markdown("---")

            # --- Step 3: Convert to Audio ---
            st.subheader("🔊 Listen to the Speech:")

            with st.spinner("🎵 Converting text to audio..."):
                lang_code = LANGUAGE_MAP.get(language.strip().lower(), "en")
                audio_bytes = text_to_audio(speech, lang_code)

            if audio_bytes:
                # Play Audio
                st.audio(audio_bytes, format="audio/mp3")

                # Download Button
                st.download_button(
                    label="⬇️ Download Speech as MP3",
                    data=audio_bytes,
                    file_name=f"{topic.replace(' ', '_')}_speech.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )

                st.success("✅ Speech generated and audio ready!")
            else:
                st.error("❌ Failed to convert text to audio.")

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# -----------------------------
# 9. Footer
# -----------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>"
    "Built with ❤️ using LangChain, OpenAI & Streamlit"
    "</p>",
    unsafe_allow_html=True
)