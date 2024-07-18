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

# from dotenv import load_dotenv
# load_dotenv()  # take environment variables from .env.

# import streamlit as st
# import os
# from PIL import Image
# import google.generativeai as genai

# # Configure the API key
# os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Initialize the chat model
# text_model = genai.GenerativeModel('gemini-pro')
# chat = text_model.start_chat(history=[])

# # Initialize the image model
# image_model = genai.GenerativeModel('gemini-pro-vision')

# def get_text_response(input_text):
#     response = chat.send_message(input_text, stream=True)
#     return response

# def get_image_response(input_text, image):
#     if input_text:
#         response = image_model.generate_content([input_text, image])
#     else:
#         response = image_model.generate_content(image)
#     return response.text

# # Initialize Streamlit app
# st.set_page_config(page_title="Gemini Application")

# st.header("Medical Text and Image Application")

# # Text Query Section
# st.subheader("Text Query")
# input_text = st.text_input("Enter your question here:", key="text_input")

# submit_text = st.button("Submit Text Query")

# if submit_text:
#     if input_text:
#         response = get_text_response(input_text)
#         st.subheader("The Response is")
#         for chunk in response:
#             st.write(chunk.text)
#             st.write("_" * 80)
#     else:
#         st.write("Please enter a question.")

# # Image Query Section
# st.subheader("Image Query")
# input_prompt = st.text_input("Enter your input prompt for the image:", key="image_input")

# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
# image = None
# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Image.", use_column_width=True)

# submit_image = st.button("Submit Image Query")

# if submit_image:
#     if image or input_prompt:
#         response = get_image_response(input_prompt, image)
#         st.subheader("The Response is")
#         st.write(response)
#     else:
#         st.write("Please provide an input prompt or upload an image.")

# ---------------------------------
from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from PyPDF2 import PdfReader
import docx
import pytesseract

load_dotenv()  # Load environment variables from .env

# Configure the Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Initialize the chat and image models
text_model = genai.GenerativeModel('gemini-pro')
chat = text_model.start_chat(history=[])
image_model = genai.GenerativeModel('gemini-pro-vision')

# Initialize the document model
document_model = genai.GenerativeModel('gemini-pro')


# Set the tesseract command path for Linux environment
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\tesseract.exe'


def get_text_response(input_text):
    response = chat.send_message(input_text, stream=True)
    return response

def get_image_response(input_text, image):
    if input_text:
        response = image_model.generate_content([input_text, image])
    else:
        response = image_model.generate_content(image)
    return response.text

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_doc(doc_file):
    doc = docx.Document(doc_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return text

def extract_text_from_images(image_files):
    # Update the path to where Tesseract is installed
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    text = ""
    for image_file in image_files:
        image = Image.open(image_file)
        text += pytesseract.image_to_string(image) + "\n"
    return text

def generate_document_response(document_text, user_prompt):
    response = document_model.generate_content([document_text, user_prompt])
    return response.text

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Application")

st.sidebar.title("Navigation")
option = st.sidebar.radio("Choose a functionality:", ["Text Query", "Image Query", "Document Summary"])

st.header("Gemini Medical Application")

if option == "Text Query":
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

elif option == "Image Query":
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

elif option == "Document Summary":
    st.subheader("Document Summary")
    doc_option = st.selectbox('Choose the type of document you want to upload:', ('PDF', 'DOCX', 'Images'))
    uploaded_files = st.file_uploader("Choose files...", type=["pdf", "docx", "jpg", "jpeg", "png"], accept_multiple_files=True)
    user_prompt = st.text_input("Enter your question or prompt regarding the document:")
    submit = st.button("Get Response")

    if submit and uploaded_files:
        document_text = ""
        if doc_option == 'PDF' and all(file.name.endswith(".pdf") for file in uploaded_files):
            for file in uploaded_files:
                document_text += extract_text_from_pdf(file)
        elif doc_option == 'DOCX' and all(file.name.endswith(".docx") for file in uploaded_files):
            for file in uploaded_files:
                document_text += extract_text_from_doc(file)
        elif doc_option == 'Images' and all(file.name.endswith(("jpg", "jpeg", "png")) for file in uploaded_files):
            document_text = extract_text_from_images(uploaded_files)
        else:
            st.error("Unsupported file type or mismatched option.")
            document_text = None

        if document_text:
            response = generate_document_response(document_text, user_prompt)
            st.subheader("Response")
            st.write(response)
        else:
            st.error("Could not extract text from the document.")
