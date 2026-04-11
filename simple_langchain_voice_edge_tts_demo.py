import os
import io
import asyncio
import edge_tts
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain_core.output_parsers import StrOutputParser

# -----------------------------
# 1. Load API Key
# -----------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("🚫 OpenAI API Key not found!")
    st.stop()

# -----------------------------
# 2. Initialize LLM
# -----------------------------
llm = ChatOpenAI(model="gpt-5", api_key=OPENAI_API_KEY)

# -----------------------------
# 3. Prompt Templates
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

# ------------------------------------------
# 5. Available Human-Like Voices (Edge TTS)
# ------------------------------------------
VOICE_OPTIONS = {
    "English - Male (Guy)": "en-US-GuyNeural",
    "English - Male (Christopher)": "en-US-ChristopherNeural",
    "English - Male (Eric)": "en-US-EricNeural",
    "English - Male (Roger)": "en-US-RogerNeural",
    "English - Female (Jenny)": "en-US-JennyNeural",
    "English - Female (Aria)": "en-US-AriaNeural",
    "English - Female (Sara)": "en-US-SaraNeural",
    "English UK - Male (Ryan)": "en-GB-RyanNeural",
    "English UK - Female (Sonia)": "en-GB-SoniaNeural",
    "English Australia - Male (William)": "en-AU-WilliamNeural",
    "English India - Male (Prabhat)": "en-IN-PrabhatNeural",
    "English India - Female (Neerja)": "en-IN-NeerjaNeural",
    "Hindi - Male (Madhur)": "hi-IN-MadhurNeural",
    "Hindi - Female (Swara)": "hi-IN-SwaraNeural",
    "Urdu - Male (Salman)": "ur-PK-SalmanNeural",
    "Urdu - Female (Uzma)": "ur-PK-UzmaNeural",
    "Spanish - Male (Alvaro)": "es-ES-AlvaroNeural",
    "Spanish - Female (Elvira)": "es-ES-ElviraNeural",
    "French - Male (Henri)": "fr-FR-HenriNeural",
    "French - Female (Denise)": "fr-FR-DeniseNeural",
    "German - Male (Conrad)": "de-DE-ConradNeural",
    "German - Female (Katja)": "de-DE-KatjaNeural",
    "Arabic - Male (Hamed)": "ar-SA-HamedNeural",
    "Arabic - Female (Zariyah)": "ar-SA-ZariyahNeural",
    "Chinese - Male (Yunyang)": "zh-CN-YunyangNeural",
    "Chinese - Female (Xiaoxiao)": "zh-CN-XiaoxiaoNeural",
    "Japanese - Male (Keita)": "ja-JP-KeitaNeural",
    "Japanese - Female (Nanami)": "ja-JP-NanamiNeural",
    "Korean - Male (InJoon)": "ko-KR-InJoonNeural",
    "Korean - Female (SunHi)": "ko-KR-SunHiNeural",
    "Portuguese - Male (Antonio)": "pt-BR-AntonioNeural",
    "Turkish - Male (Ahmet)": "tr-TR-AhmetNeural",
    "Italian - Male (Diego)": "it-IT-DiegoNeural",
}

# ------------------------------------------
# 6. Text to Audio Function (Edge TTS)
# ------------------------------------------
async def text_to_audio_edge(text, voice_name):
    """
    Convert text to audio using Microsoft Edge TTS.
    Returns audio as BytesIO object.
    Uses modern, natural human-like voices.
    """
    communicate = edge_tts.Communicate(text=text, voice=voice_name)
    audio_buffer = io.BytesIO()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk["data"])

    audio_buffer.seek(0)
    return audio_buffer


def generate_audio(text, voice_name):
    """Wrapper to run async function in sync context"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio = loop.run_until_complete(
            text_to_audio_edge(text, voice_name)
        )
        loop.close()
        return audio
    except Exception as e:
        st.error(f"Audio error: {str(e)}")
        return None

# -----------------------------
# 7. Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="AI Speech Generator",
    page_icon="🎤",
    layout="centered"
)

st.title("🎤 AI Speech Generator")
st.markdown("Generate a powerful speech and listen with **human-like voice!**")
st.markdown("---")

# --- Input Fields ---
topic = st.text_input(
    "📌 Enter a Topic:",
    placeholder="e.g., Climate Change, Education, Technology"
)

language = st.text_input(
    "🌐 Enter a Language:",
    placeholder="e.g., English, Hindi, Spanish, Urdu"
)

# --- Voice Selection ---
st.markdown("### 🎙️ Choose a Voice:")
selected_voice_label = st.selectbox(
    "Select a modern human-like voice:",
    options=list(VOICE_OPTIONS.keys()),
    index=0  # Default: English Male (Guy)
)

selected_voice_id = VOICE_OPTIONS[selected_voice_label]

# Show selected voice info
st.info(f"🎙️ Selected Voice: **{selected_voice_label}** (`{selected_voice_id}`)")

generate_btn = st.button("🚀 Generate Speech", use_container_width=True)

# -----------------------------
# 8. Handle Generation
# -----------------------------
if generate_btn:
    if not topic or not language:
        st.warning("⚠️ Please fill in both Topic and Language fields.")
    else:
        try:
            # --- Generate Title ---
            with st.spinner("✍️ Generating title..."):
                title = title_chain.invoke({
                    "topic": topic,
                    "language": language
                })

            st.subheader("🏆 Generated Title:")
            st.success(f"**{title}**")

            # --- Generate Speech ---
            with st.spinner("📝 Writing speech content..."):
                speech = speech_chain.invoke({
                    "title": title,
                    "language": language
                })

            st.subheader("📝 Full Speech:")
            st.markdown(speech)

            st.markdown("---")

            # --- Convert to Audio ---
            st.subheader("🔊 Listen to the Speech:")

            with st.spinner("🎵 Converting to human-like audio..."):
                audio_bytes = generate_audio(speech, selected_voice_id)

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

                st.success("✅ Speech generated with human-like voice!")
            else:
                st.error("❌ Failed to generate audio.")

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>"
    "Built with ❤️ using LangChain, OpenAI & Edge TTS"
    "</p>",
    unsafe_allow_html=True
)