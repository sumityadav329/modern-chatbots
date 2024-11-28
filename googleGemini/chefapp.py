import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv('API_KEY'))

# Function to load Google Gemini Vision Pro
def get_gemini_response(image, prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-8b")
    response = model.generate_content([image[0], prompt])
    return response.text

# Function to process uploaded images
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        import_parts = [
            {
                "mime_type": uploaded_file.type,  # Get MIME type of uploaded file
                "data": bytes_data
            }
        ]
        return import_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit app setup
st.set_page_config(page_title="Recipe Checker", page_icon="🍴", layout="centered")

# Header and app introduction
st.title("🍴 Recipe Checker with Gemini Vision")
st.markdown(
    """
    **Upload an image of a recipe or dish, and let our AI describe it in detail!**
    \nThis app uses the **Google Gemini Vision model** to identify ingredients, provide recipe details, and nutritional information.
    """
)

# Input fields
uploaded_file = st.file_uploader("Upload a recipe image (JPG, JPEG, PNG):", type=['jpg', 'jpeg', 'png'])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Prompt for recipe analysis
input_prompt = """
You are an expert chef. Analyze the given image of the dish and provide:
1. The name of the dish (if possible).
2. A detailed list of ingredients.
3. Steps for preparing the dish.
4. Additional tips or variations for the recipe.
"""

# Button to generate response
if st.button("Analyze Recipe"):
    if uploaded_file:
        try:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(image_data, input_prompt)
            st.subheader("🍽 Recipe Analysis")
            st.markdown(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload an image to proceed.")

# Footer
st.markdown(
    """
    ---
    **Powered by [Google Gemini Vision](https://ai.google/tools/).**
    """
)
