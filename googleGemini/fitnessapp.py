import streamlit as st
import base64
from PIL import Image
from io import BytesIO
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv('API_KEY'))

# Function to generate food analysis
def analyze_food_image(image):
    try:
        # Prepare the model
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        
        # Detailed prompt for nutritional analysis
        input_prompt = """
        You are an expert nutritionist and food analyst. Carefully examine the food image and provide:
        1. Detailed list of food items identified
        2. Calories for each item
        3. Nutritional breakdown (protein, carbs, fats)
        4. Estimated total calorie count
        5. Brief health insights or recommendations

        Format your response clearly with headings and bullet points.
        """
        
        # Generate content
        response = model.generate_content([input_prompt, image, "Analyze in detail"])
        return response.text
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

# Streamlit App Configuration
st.set_page_config(
    page_title="Food Calorie Analyzer", 
    page_icon="🍽️", 
    layout="wide"
)

# Main App
def main():
    # Custom CSS for ChatGPT-like interface
    st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stTextInput>div>div>input {
        background-color: #f9f9f9;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Title and Description
    st.title("🍽️ AI Food Calorie Analyzer")
    st.markdown("*Upload a photo of your meal and get detailed nutritional insights!*")

    # Sidebar for additional information
    with st.sidebar:
        st.header("How It Works")
        st.write("""
        1. Upload a clear image of your food
        2. Our AI will analyze the image
        3. Receive detailed nutritional information
        """)
        st.info("Best results with clear, well-lit food images")

    # Main content area
    col1, col2 = st.columns(2)

    with col1:
        st.header("Upload Image")
        # Image Upload
        uploaded_file = st.file_uploader(
            "Choose a food image", 
            type=['jpg', 'jpeg', 'png'],
            help="Upload a clear image of your meal"
        )

    with col2:
        st.header("Nutritional Analysis")
        # Analysis Display Area
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)

            # Analyze Button
            if st.button("Analyze Nutritional Content", type="primary"):
                with st.spinner('Analyzing your meal...'):
                    # Perform analysis
                    analysis_result = analyze_food_image(image)
                    
                    # Display results in a chat-like interface
                    st.markdown("""
                    <div class="chat-container">
                        <div style="background-color:#e6f2ff; padding:15px; border-radius:10px; margin-bottom:10px;">
                            <strong>🤖 AI Nutritionist:</strong>
                        </div>
                        <div style="background-color:#f9f9f9; padding:15px; border-radius:10px;">
                    """, unsafe_allow_html=True)
                    
                    # Display analysis result
                    st.markdown(analysis_result)
                    
                    st.markdown("</div>", unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()