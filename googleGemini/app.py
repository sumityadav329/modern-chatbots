from flask import Flask, request, jsonify
import base64
from PIL import Image
from io import BytesIO
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

genai.configure(api_key=os.getenv('API_KEY'))

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    image_data = data.get('image')
    image = Image.open(BytesIO(base64.b64decode(image_data.split(',')[1])))

    input_prompt = """
    You are an expert nutritionist. Analyze the food items in the image
    and calculate the total calories. Also, provide the details of each food item with calories intake in the following format:
    1. Item 1 - number of calories
    2. Item 2 - number of calories
    -----
    -----
    """
    
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    response = model.generate_content([input_prompt, image, ""])  # Replace "" with any additional prompt if necessary
    
    return jsonify({'result': response.text})

if __name__ == '__main__':
    app.run(debug=True)
