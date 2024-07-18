# # Q&A Chatbot
# #from langchain.llms import OpenAI

# from dotenv import load_dotenv

# load_dotenv()  # take environment variables from .env.

# import streamlit as st
# import os
# import pathlib
# import textwrap
# from PIL import Image


# import google.generativeai as genai


# os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ## Function to load OpenAI model and get respones

# def get_gemini_response(input,image):
#     model = genai.GenerativeModel('gemini-pro-vision')
#     if input!="":
#        response = model.generate_content([input,image])
#     else:
#        response = model.generate_content(image)
#     return response.text

# ##initialize our streamlit app

# st.set_page_config(page_title="Medical Image Demo")

# st.header("Gemini Application")
# input=st.text_input("Input Prompt: ",key="input")
# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
# image=""   
# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Image.", use_column_width=True)


# submit=st.button("Tell me about the image")

# ## If ask button is clicked

# if submit:
    
#     response=get_gemini_response(input,image)
#     st.subheader("The Response is")
#     st.write(response)

# ---------------------------------
# For chatbot and image input

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Configure the API key
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the chat model
text_model = genai.GenerativeModel('gemini-pro')
chat = text_model.start_chat(history=[])

# Initialize the image model
image_model = genai.GenerativeModel('gemini-pro-vision')

def get_text_response(input_text):
    response = chat.send_message(input_text, stream=True)
    return response

def get_image_response(input_text, image):
    if input_text:
        response = image_model.generate_content([input_text, image])
    else:
        response = image_model.generate_content(image)
    return response.text

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Application")

st.header("Medical Text and Image Application")

# Text Query Section
st.subheader("Text Query")
input_text = st.text_input("Enter your question here:", key="text_input")

submit_text = st.button("Submit Text Query")

if submit_text:
    if input_text:
        response = get_text_response(input_text)
        st.subheader("The Response is")
        for chunk in response:
            st.write(chunk.text)
            st.write("_" * 80)
    else:
        st.write("Please enter a question.")

# Image Query Section
st.subheader("Image Query")
input_prompt = st.text_input("Enter your input prompt for the image:", key="image_input")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit_image = st.button("Submit Image Query")

if submit_image:
    if image or input_prompt:
        response = get_image_response(input_prompt, image)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please provide an input prompt or upload an image.")


# ---------------------------------
