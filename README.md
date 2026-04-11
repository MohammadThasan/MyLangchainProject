# 🤖 MyLangchainProject

A collection of Python demo scripts exploring **LangChain**, **Streamlit**, **OpenAI**, and **Ollama** to build AI-powered applications — from simple Q&A bots to full speech generators with text-to-speech audio.

---

## 📂 Project Structure

| File | Description |
|------|-------------|
| `app.py` | A minimal Streamlit "Hello World" starter app with user text input |
| `openai_demo.py` | Basic CLI chatbot using OpenAI GPT-4o-mini via LangChain |
| `ollama_demo.py` | Basic CLI chatbot using a local Ollama model (Qwen 3.5 4B) |
| `streamlit_demo.py` | Simple Streamlit Q&A app powered by OpenAI |
| `streamlit_local_LLM_demo.py` | Simple Streamlit Q&A app powered by local Ollama |
| `prompt_template_demo.py` | Cuisine info app using LangChain **PromptTemplates** + OpenAI + Streamlit |
| `local_prompt_template_LLM_demo.py` | Same cuisine app but using a **local Ollama** model instead of OpenAI |
| `travel_app_demo.py` | AI Travel Guide Generator (OpenAI) — city, month, language & budget inputs |
| `ollama_travel_app_demo.py` | AI Travel Guide Generator using **Ollama (Qwen 3.5 4B)** |
| `local_ollama_travel_app_demo.py` | AI Travel Guide Generator using **Ollama (Gemma 3 4B)** |
| `simplechain_demo.py` | Speech Generator using LangChain **chains** — title → speech pipeline |
| `simplechain_demo_with_Lamda_for_title.py` | Speech Generator using a **lambda** in the chain to display the title mid-pipeline |
| `simplechain_demo_doubl_variables.py` | Speech Generator with **multi-variable** chains (topic + language) and LangChain debug mode |
| `multiple_llm_demo.py` | Speech Generator using **two different LLMs** (OpenAI for title → Ollama for speech) |
| `blog_post_generator_demo.py` | Blog Post Generator: outline → introduction → **OpenAI TTS audio** with download |
| `multi_llm_blog_post_generator_demo.py` | Blog Post Generator using **multi-LLM** (OpenAI outline → Ollama intro → OpenAI TTS) |
| `simplechain_audio_demo_doubl_variables.py` | Speech Generator with **gTTS** (Google Text-to-Speech) audio output |
| `simple_langchain_voice_gtts_demo.py` | Speech Generator with **OpenAI TTS** audio and voice selection |
| `simple_langchain_voice_edge_tts_demo.py` | Speech Generator with **Edge TTS** — 30+ human-like voices in multiple languages |
| `mindful_morning_coach.py` | 🧘 Mindful Morning Coach — mood-based motivational notes with dynamic UI themes |

---

## 🧰 Tech Stack

- **[LangChain](https://www.langchain.com/)** — Framework for building LLM-powered applications (prompt templates, chains, output parsers)
- **[Streamlit](https://streamlit.io/)** — Python framework for building interactive web UIs
- **[OpenAI API](https://platform.openai.com/)** — Cloud-based LLM (GPT-4o-mini / GPT-5) and Text-to-Speech (TTS-1)
- **[Ollama](https://ollama.com/)** — Run open-source LLMs locally (Gemma 3, Qwen 3.5)
- **[Edge TTS](https://pypi.org/project/edge-tts/)** — Free Microsoft Edge text-to-speech with 30+ natural voices
- **[gTTS](https://pypi.org/project/gTTS/)** — Google Text-to-Speech for audio generation

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed (for local LLM demos)

### Installation

```bash
# Clone the repository
git clone https://github.com/MohammadThasan/MyLangchainProject.git
cd MyLangchainProject

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install langchain langchain-openai langchain-community streamlit openai gtts edge-tts
```

### Environment Variables

Set your OpenAI API key (required for OpenAI-based demos):

```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY = "sk-your-key-here"

# macOS/Linux
export OPENAI_API_KEY="sk-your-key-here"
```

### Pull Local Models (for Ollama demos)

```bash
ollama pull gemma3:4b
ollama pull qwen3.5:4b
```

---

## ▶️ Running the Apps

Most scripts are **Streamlit** apps. Run them with:

```bash
streamlit run app.py
streamlit run blog_post_generator_demo.py
streamlit run mindful_morning_coach.py
# ... etc.
```

CLI-based scripts (no Streamlit):

```bash
python openai_demo.py
python ollama_demo.py
```

---

## 📚 Key Concepts Covered

| Concept | Description |
|---------|-------------|
| **Prompt Templates** | Reusable prompts with `{placeholders}` filled by user input |
| **LangChain Chains** | Piping output from one step to the next (`prompt \| llm \| parser`) |
| **Multi-LLM Pipelines** | Using different models for different tasks in a single workflow |
| **Output Parsers** | Extracting clean text from LLM responses with `StrOutputParser` |
| **Text-to-Speech** | Converting AI-generated text to audio (OpenAI TTS, Edge TTS, gTTS) |
| **Lambda in Chains** | Using Python lambdas for side effects (e.g., displaying titles mid-chain) |
| **Debug Mode** | LangChain's `set_debug(True)` to inspect prompts, responses & token usage |

---

## 📝 License

This project is for **educational and personal learning** purposes.

---

## 🙏 Acknowledgements

Built with ❤️ using [LangChain](https://www.langchain.com/), [OpenAI](https://openai.com/), [Ollama](https://ollama.com/) & [Streamlit](https://streamlit.io/).
