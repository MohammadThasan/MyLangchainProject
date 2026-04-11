import streamlit as st
import random
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate

# --- Initialize LLM (Local Ollama) ---
# Make sure your local Ollama app is running and you have pulled the model!
# Command line: ollama run gemma3:4b
llm = ChatOllama(model="gemma3:4b")

# --- App Setup ---
st.set_page_config(page_title="🧘 Mindful Morning Coach", layout="centered")

# --- Mood-based Color Palettes & Backgrounds ---
mood_colors = {
    "Calm": "#B3E5FC",
    "Stressed": "#FFE0B2",
    "Grateful": "#C8E6C9",
    "Motivated": "#FFF59D",
    "Tired": "#E1BEE7",
    "Reflective": "#FFCCBC",
}

backgrounds = [
    "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
    "linear-gradient(135deg, #c3cfe2 0%, #c3f0ca 100%)",
    "linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%)",
    "linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%)",
]

# Apply random background
bg_choice = random.choice(backgrounds)
st.markdown(
    f"""
    <style>
    .stApp {{
        background: {bg_choice};
        color: #333333;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Title Section ---
st.title("🧘 Mindful Morning Coach")
st.subheader("Start your day with calm, focus, and intention 🌞")
st.write("Tell me how you feel and what you want to focus on today.")

# --- User Inputs ---
mood = st.selectbox(
    "💭 How are you feeling right now?",
    list(mood_colors.keys())
)

goals = st.text_input("🎯 What's your focus or goal for today?",
                      placeholder="e.g., stay positive, finish a key task, be present")
time_of_day = st.selectbox("⏰ Time of day", ["Morning", "Afternoon", "Evening"])

# --- Background Color Indicator Based on Mood ---
if mood:
    color = mood_colors.get(mood, "#FFFFFF")
    st.markdown(f"<div style='background-color:{color};padding:10px;border-radius:10px;margin-bottom:15px;'></div>",
                unsafe_allow_html=True)

# --- Button & Generation Logic ---
if st.button("🌸 Get My Mindful Note"):
    if not mood or not goals:
        st.warning("Please select your mood and enter your goal for the day.")
    else:
        with st.spinner("Breathing in calm energy... ✨"):

            prompt_template = PromptTemplate(
                input_variables=["mood", "goals", "time_of_day"],
                template="""You are a supportive, mindful coach. 
                The user is feeling {mood} this {time_of_day}. 
                Their focus for today is: {goals}. 
                Write a short, highly empathetic, and actionable 3-sentence note to guide their mindset."""
            )

            formatted_prompt = prompt_template.format(
                mood=mood, goals=goals, time_of_day=time_of_day
            )

            # Generate Response via Local Ollama
            response = llm.invoke(formatted_prompt)

            # Display Output
            st.markdown("### 🌤️ Your Mindful Moment")
            st.write(response.content)

            # Optional Download
            st.download_button(
                label="💌 Save Reflection",
                data=response.content,
                file_name=f"mindful_note_{time_of_day.lower()}.txt",
                mime="text/plain"
            )

# --- Footer ---
st.markdown("---")
st.caption("🌻 Created with love using Local Ollama + Streamlit | By [Your Name]")