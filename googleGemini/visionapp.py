
import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import google.generativeai as genai


load_dotenv() # load all the environment variables

genai.configure(api_key=os.getenv('API_KEY'))

# function to load google gemini vision pro

def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):

    if uploaded_file is not None:
        #read the file into bytes
        bytes_data = uploaded_file.getvalue()

        import_parts = [
            {
                "mime_type": uploaded_file.type, # get the mime type of the uploaded file
                "data":bytes_data
            }
        ]
        return import_parts
    else:
        raise FileNotFoundError("No file uploaded")

# initialize streamlit app

st.set_page_config(page_title= "Gemini Health App")

st.header("Health App using Gemini Vision Model")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=['jpg','jpeg','png'])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption = "Uplaoded Image.", use_column_width=True)

submit = st.button("Tell me about the calories")

input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image
            and calculate the total calories, also provide the details of every food items with calories intake
            is below format
             1. Item 1 - no of calories
             2. Item 2 - no of calories
             -----
             -----
            
"""      

# if submit button is clicked 

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The response is  ")
    st.write(response)

