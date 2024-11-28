import os
import logging
from flask import Flask, request, render_template
import requests
from dotenv import load_dotenv

# Configure logging for debugging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
API_TOKEN = os.getenv('HF_TOKEN')

# Ensure headers include authorization token
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query_hf(payload):
    """
    Send a request to the Hugging Face API and return the response.
    Includes detailed logging for debugging.
    """
    try:
        logger.debug(f"Payload sent to API: {payload}")
        response = requests.post(API_URL, headers=headers, json=payload)
        
        # Log API response details
        logger.debug(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Headers: {response.headers}")
        logger.debug(f"Response Content: {response.text}")
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        logger.error(f"API Request Error: {e}")
        return {"error": str(e)}


chat_history = []


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handle GET and POST requests for the chat application.
    GET: Renders the chat interface.
    POST: Processes user input and updates chat history.
    """
    global chat_history
    
    if request.method == 'POST':
        user_input = request.form.get('message', '').strip()
        logger.info(f"Received user input: {user_input}")

        if not user_input:
            return render_template('index.html', chat_history=chat_history)

        # Add user input to chat history
        chat_history.append({"role": "user", "content": user_input})

        # Prepare chat history as conversation context
        conversation = "\n".join(
            [f"{entry['role']}: {entry['content']}" for entry in chat_history]
        )

        # Payload for the API
        payload = {
            "inputs": conversation,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.7
            }
        }

        # Query the Hugging Face API
        response = query_hf(payload)
        logger.debug(f"API Response: {response}")

        # Parse the response
        if isinstance(response, list) and response:
            bot_response = response[0].get('generated_text', 'No response generated.')
        elif isinstance(response, dict):
            if 'generated_text' in response:
                bot_response = response['generated_text']
            elif 'error' in response:
                bot_response = f"API Error: {response['error']}"
                logger.error(bot_response)
            else:
                bot_response = "Unexpected response format."
        else:
            bot_response = "Could not process the response."

        # Add bot response to chat history
        chat_history.append({"role": "assistant", "content": bot_response})

        return render_template('index.html', chat_history=chat_history)

    # For GET requests, reset chat history and render the chat interface
    chat_history.clear()
    return render_template('index.html', chat_history=chat_history)


if __name__ == '__main__':
    app.run(debug=True)
