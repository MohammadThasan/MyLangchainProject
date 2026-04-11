import os
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Check if API key is available
if not OPENAI_API_KEY:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# 1: Changed model from "gpt-5" to a valid model name
# gpt-5 doesn't exist yet. Use gpt-4, gpt-4-turbo, or gpt-3.5-turbo
llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)  # or "gpt-4", "gpt-3.5-turbo"

# 2: Removed the extra Assistant message that was causing issues
# The prompt template should only have system and human messages
# The assistant's response will come from the LLM, not be hardcoded
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an Agile coach. You can answer any questions related to Agile process. Don't answer any questions if they are not related to Agile process. If user asks such questions, just say 'I don't know'."),
        ("human", "{input}")
    ]
)

st.title("Agile Coach")

# 3: Changed variable name from 'input' to 'user_input' to avoid
# shadowing Python's built-in input() function
user_input = st.text_input("Please enter your question")

chain = prompt_template | llm

# 4: Use the renamed variable
if user_input:
    # Show greeting first
    st.write("🤝 Thank you so much for connecting with us! I will be happy to help.")
    with st.spinner("Thinking..."):
        try:
            response = chain.invoke({"input": user_input})
            st.write(response.content)  # Only runs if no error
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")  # Shows friendly error
            # App keeps running! User can try again