import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('API_KEY'))

# Load Gemini model and start chat
model = genai.GenerativeModel(model_name="gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(query):
    try:
        response = chat.send_message(query, stream=True)
        return response
    except Exception as e:
        return [{"text": f"Error: {e}"}]

# Streamlit app setup
st.set_page_config(page_title="AI Code Explainer & Debugger", page_icon="💻", layout="wide")

# Header and introduction
st.title("💻 AI Code Explainer & Debugger")
st.markdown(
    """
    **Welcome to the AI Code Explainer & Debugger!**  
    Paste your code snippet below, and our advanced Gemini model will explain or debug it.  
    Perfect for learning, troubleshooting, or optimizing your code.
    """
)

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Input box for code snippets
st.divider()
code_snippet = st.text_area(
    "Paste your code snippet below:",
    key="code_input",
    height=200,
    placeholder="def greet(name):\n    return f'Hello, {name}!'"
)

task = st.radio(
    "What do you want the AI to do?",
    options=["Explain the Code", "Debug the Code", "Optimize the Code"],
    horizontal=True,
    key="task_selection"
)

submit_query = st.button("Analyze Code")

# Handle user input and generate response
if submit_query and code_snippet.strip():
    # Add user task and code snippet to chat history
    user_task = f"Task: {task}\nCode:\n{code_snippet}"
    st.session_state["chat_history"].append(("user", user_task))
    st.chat_message("user").markdown(f"**Task:** {task}\n```python\n{code_snippet}\n```")

    # Generate and display bot response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        query = f"Please {task.lower()} the following Python code:\n\n{code_snippet}"
        response_stream = get_gemini_response(query)
        bot_response = ""
        for chunk in response_stream:
            bot_response += chunk.text
            placeholder.markdown(f"**AI Response:**\n```\n{bot_response}\n```")

    # Add bot response to chat history
    st.session_state["chat_history"].append(("bot", bot_response))

# Display the chat conversation dynamically
st.divider()
st.subheader("Chat History")
for role, message in st.session_state["chat_history"]:
    if role == "user":
        st.chat_message("user").markdown(f"**You:**\n{message}")
    else:
        st.chat_message("assistant").markdown(f"**Gemini:**\n```python\n{message}\n```")

# Footer
st.markdown(
    """
    ---
    **Developed with [Google Gemini AI](https://ai.google/tools/) and Streamlit.**  
    Powered by generative AI for developers.
    """
)
