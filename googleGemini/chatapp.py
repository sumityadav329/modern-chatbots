from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv('API_KEY'))

# function to load Gemini pro model and get response
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def get_gemini_response(query):
    response= chat.send_message(query,stream=True)
    return response


# initialize our streamlit app

st.set_page_config(page_title="Q&A Demo")

st.header("Gemini AI Chatbot")

# initialize session state for the chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state["chat_history"] = []

input = st.text_input("Input:", key="input")
submit = st.button("Ask the Query")

if submit and input:
    response = get_gemini_response(input)
    # add user query  and response to session chat history
    st.session_state["chat_history"].append(("You",input))
    st.subheader("The Response is ")
    for chunk in response:
        st.write(chunk.text)
        st.session_state["chat_history"].append(("Bot", chunk.text))
st.subheader("The Chat History is ")

for role, text in st.session_state["chat_history"]:
    st.write(f"{role}: {text}")