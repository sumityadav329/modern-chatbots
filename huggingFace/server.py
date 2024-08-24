from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
API_TOKEN = os.getenv('HF_API_TOKEN')

headers = {}
if API_TOKEN:
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # Debug: Print the raw response
    print("API Response:", response.json())
    
    return response.json()

chat_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global chat_history
    if request.method == 'POST':
        user_input = request.form['message']
        chat_history.append({"role": "user", "content": user_input})

        # Prepare the conversation history for the model
        conversation = "\n".join(
            [f"{entry['role']}: {entry['content']}" for entry in chat_history]
        )

        payload = {
            "inputs": conversation,
            "options": {"wait_for_model": True}
        }

        response = query(payload)

        # Check the structure of the response and extract the generated text
        if isinstance(response, dict):
            if 'generated_text' in response:
                bot_response = response['generated_text']
            elif 'conversation' in response and 'generated_responses' in response['conversation']:
                bot_response = response['conversation']['generated_responses'][-1]
            else:
                bot_response = 'Sorry, I did not understand that.'
        elif isinstance(response, list) and len(response) > 0 and 'generated_text' in response[0]:
            bot_response = response[0]['generated_text']
        else:
            bot_response = 'Sorry, I did not understand that.'

        chat_history.append({"role": "assistant", "content": bot_response})

        return render_template('index.html', chat_history=chat_history)
    else:
        chat_history = []
        return render_template('index.html', chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True)
