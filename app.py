# Import Streamlit
import streamlit as st

# Page title
st.title("Welcome to My First AI App")

# Display greeting
st.write("Hello World! 👋")

# Add section header
st.header("User Input Section")

# Text input box
user_name = st.text_input("Enter your name:", value="")

# Only show message if name is entered
if user_name:
    st.success(f"Hi {user_name}, welcome to Streamlit!")  # Success message