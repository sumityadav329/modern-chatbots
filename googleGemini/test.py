import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('API_KEY'))

# Load Gemini model and start chat
model = genai.GenerativeModel(model_name="gemini-1.5-flash-8b")
chat = model.start_chat(history=[])

def get_gemini_response(query):
    try:
        response = chat.send_message(query, stream=True)
        return response
    except Exception as e:
        return [{"text": f"Error: {e}"}]

# Streamlit app setup
st.set_page_config(page_title="Gemini AI Chatbot", page_icon="🤖", layout="centered")

# Header and introduction
st.title("🤖 Gemini AI Chatbot")
st.markdown(
    """
    **Welcome to the Gemini AI Chatbot!**  
    Ask any question, and our advanced Gemini model will respond in real-time.  
    Scroll up to review your conversation.
    """
)

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Display the chat conversation dynamically
st.divider()
with st.container():
    for role, message in st.session_state["chat_history"]:
        if role == "user":
            st.chat_message("user").markdown(f"**You:** {message}")
        else:
            st.chat_message("assistant").markdown(f"**Gemini:** {message}")

# Input box for user queries at the bottom
st.divider()
user_input = st.text_input("Type your query below:", key="user_input", placeholder="Ask me anything...")
submit_query = st.button("Ask", key="submit_query")

# Handle user input and generate response
if submit_query and user_input.strip():
    # Add user message to chat history
    st.session_state["chat_history"].append(("user", user_input))
    st.chat_message("user").markdown(f"**You:** {user_input}")

    # Generate and display bot response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        response_stream = get_gemini_response(user_input)
        bot_response = ""
        for chunk in response_stream:
            bot_response += chunk.text
            placeholder.markdown(f"**Gemini:** {bot_response}")

    # Add bot response to chat history
    st.session_state["chat_history"].append(("bot", bot_response))

# Footer
st.markdown(
    """
    ---
    **Developed with [Google Gemini AI](https://ai.google/tools/) and Streamlit.**  
    Powered by generative AI.
    """
)
