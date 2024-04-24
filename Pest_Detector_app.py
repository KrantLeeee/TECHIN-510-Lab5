import io
import os
import streamlit as st
import base64
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai
import pathlib
import textwrap
from IPython.display import display
from IPython.display import Markdown


# Load environment variables
load_dotenv()

# Configure the Gemini API with your Google API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))  # Ensure this matches your .env file key
model = genai.GenerativeModel('gemini-pro-vision')

def to_markdown(text):
    text = text.replace('•', ' *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Streamlit interface for uploading an image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.')

    # Convert the image to RGB if it is RGBA (to handle transparency)
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    
    # Call the Gemini API and handle the response
    try:
        response = model.generate_content(["Please recognize and only the race of the pest in the image. Then write a report in the following format: 1. Type/Race of the pest; 2. Number of the pest shown; 3. How to reduce the pest's damage over the crop.", image], stream=True)
        response.resolve()
        lines = response.text.split('\n')
        print(lines)
        report_1 = f"**Pest:** {lines[0][3:]}"
        st.markdown(report_1)
        report_2 = f"**Number:** {lines[1][3:]}"
        st.markdown(report_2)
        report_3 = f"**Advice:** {lines[2][3:]}"
        st.markdown(report_3)



    except Exception as e:
        st.error(f"Failed to call Gemini API: {str(e)}")
