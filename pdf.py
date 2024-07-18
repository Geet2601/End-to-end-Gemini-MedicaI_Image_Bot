from dotenv import load_dotenv
import streamlit as st
import os
from PyPDF2 import PdfReader
import docx
import google.generativeai as genai
from PIL import Image
import pytesseract

load_dotenv()  # Load environment variables from .env

# Configure the Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-pro')

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

def generate_response(document_text, user_prompt):
    response = model.generate_content([document_text, user_prompt])
    return response.text

# Initialize Streamlit app
st.set_page_config(page_title="Document Summary Bot")

st.header("Document Summary Bot")

option = st.selectbox(
    'Choose the type of document you want to upload:',
    ('PDF', 'DOCX', 'Images')
)

uploaded_files = st.file_uploader("Choose files...", type=["pdf", "docx", "jpg", "jpeg", "png"], accept_multiple_files=True)
user_prompt = st.text_input("Enter your question or prompt regarding the document:")
submit = st.button("Get Response")

if submit and uploaded_files:
    document_text = ""
    if option == 'PDF' and all(file.name.endswith(".pdf") for file in uploaded_files):
        for file in uploaded_files:
            document_text += extract_text_from_pdf(file)
    elif option == 'DOCX' and all(file.name.endswith(".docx") for file in uploaded_files):
        for file in uploaded_files:
            document_text += extract_text_from_doc(file)
    elif option == 'Images' and all(file.name.endswith(("jpg", "jpeg", "png")) for file in uploaded_files):
        document_text = extract_text_from_images(uploaded_files)
    else:
        st.error("Unsupported file type or mismatched option.")
        document_text = None

    if document_text:
        response = generate_response(document_text, user_prompt)
        st.subheader("Response")
        st.write(response)
    else:
        st.error("Could not extract text from the document.")
