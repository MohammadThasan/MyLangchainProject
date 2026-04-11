# Part 1: Basic Imports

import os #Access environment variables (like API keys)
from langchain_openai import ChatOpenAI #Connects to OpenAI's GPT models
import streamlit as st #Creates the web app interface
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  #A "slot" where chat history will be inserted
                                                                            # #Structures the conversation prompt
from langchain_community.chat_message_histories import StreamlitChatMessageHistory #Stores chat history in Streamlit's memory
from langchain_core.runnables.history import RunnableWithMessageHistory #Wraps chain to automatically handle history

# Part 2: Setup the Model and Prompt
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system","You are an Science coach, you can answer any questions related to Science subject. Dont answer any questions if they are not related to Science subject. If user asks such questions, just say, I dont know"),
        MessagesPlaceholder(variable_name="chat_history"), # Key concept -> The MessagesPlaceholder is crucial! It's like a bookmark where the chat history will be inserted:
        ("human","{input}") # <- Current question
    ]
)
# Part 3: Create the Chai
# The pipe operator | chains components together: Prompt → LLM
chain = prompt_template | llm

# Part 4: Set Up History Storage
# What this does: Creates an empty list that will store all messages:
# Internally, it looks like this:
# history_for_chain.messages = [
    # HumanMessage(content="What is photosynthesis?"),
    # AIMessage(content="Photosynthesis is the process..."),
    # HumanMessage(content="How does it work?"),
    # AIMessage(content="It works by converting...")
# ]

history_for_chain = StreamlitChatMessageHistory()

# Part 5: Wrap Chain with History (MOST IMPORTANT)
# What this does: Creates an automatic system that:
# 1. Before each AI call, it injects the chat history into the MessagesPlaceholder
# 2. After each AI response, it saves both question and answer to history

chain_with_history = RunnableWithMessageHistory(
    chain,                                    # Your AI chain
    lambda session_id: history_for_chain,     # Where to store history
    input_messages_key="input",               # Which key has the new message
    history_messages_key="chat_history"       # Which placeholder gets history
)
# Visuals Example:
# User asks: "What is photosynthesis?"
#         ↓
# [1] Get history (empty for first question)
#         ↓
# [2] Inject into prompt: system + history + "What is photosynthesis?"
#          ↓
# [3] AI generates response
#          ↓
# [4] Save to history: (Human: "What is photosynthesis?", AI: "Photosynthesis is...")
#          ↓
# User asks: "How does it work?"
#          ↓
# [1] Get history (now has previous Q&A)
#         ↓
# [2] Inject into prompt: system + [previous Q&A] + "How does it work?"
#         ↓
# [3] AI generates response with context!

# Part 6: Streamlit UI
st.title("Science Coach")
input = st.text_input("Enter your question")

# Part 7: Invoke the Chain
# The session_id: Allows multiple independent conversations:
if input:
    response = chain_with_history.invoke(
        {"input": input},                    # Current question
        {"configurable": {"session_id": "abc123"}}  # Session identifier
    )
    st.write(response.content)

# Part 8: Display History
st.write("HISTORY")
st.write(history_for_chain)  # Shows all stored messages

# Adding a clear history button
if st.button("Clear History"):
    history_for_chain.clear()
    st.rerun()

# Display history in a nicer format
st.write("### Conversation History")
for msg in history_for_chain.messages:
    st.write(f"**{msg.type}:** {msg.content}")

# Showing how many messages are stored
st.write(f"Total messages in history: {len(history_for_chain.messages)}")