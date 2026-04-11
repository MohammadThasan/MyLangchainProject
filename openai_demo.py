# Import the os module to work with operating system related features
import os

# Import OpenAI's chat model interface from LangChain
from langchain_openai import ChatOpenAI

# Retrieve your API Key from environment variables
# NEVER hardcode your API key in the script for security reasons
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if the API key was found; otherwise warn the user
if not OPENAI_API_KEY:
    print("⚠️  Warning: Please set your OpenAI API Key.")
    print('Set your key like this: export OPENAI_API_KEY="sk-..."')
    # Comment: In a real app, you could abort execution here with sys.exit(1)

# Initialize the Large Language Model (LLM)
# Uses the 'gpt-4o-mini' model (a lightweight GPT-4 variant)
llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

# Get the user's question interactively via command line
question = input("What is your question? ")

# Send the question to the model and store the raw completion result
response = llm.invoke(question)

# Display the full response object for debugging/inspection purposes
print("Full Response Object:\n", response)

# Extract just the generated text content for clean output
print("\nModel's Reply:")
print(response.content if hasattr(response, 'content') else response)