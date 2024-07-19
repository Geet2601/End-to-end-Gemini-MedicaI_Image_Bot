from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from PyPDF2 import PdfReader
import docx
import pytesseract
import base64


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
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

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



@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
img = get_img_as_base64("bg02.jpg")
img01 = get_img_as_base64("side02.jpg")

# Load and apply custom CSS
# with open("designing.css") as source_des:
#     st.markdown(f"<style>{source_des.read()}</style>",
#     unsafe_allow_html=True)

page_by_img = f""" 
<style>
[data-testid="stAppViewContainer"]
{{
background-color:red;
background-image: url("data:bg02/jpg;base64,{img}");
backgroud-size:cover;

}}
[data-testid="stHeader"]
{{
background-color: rgba(0, 0, 0, 0);
}}
[id="medical-application"]
{{
color: rgb(222, 186, 255);
font-weight: bolder;

}}
[id="medical-chatbot"]
{{
color: rgb(222, 208, 235);
}}
[data-testid="stTextInput-RootElement"]
{{
border-radius:50px;
border-width:2px;
border-color: rgb(222, 125, 178);
}}
[data-baseweb="base-input"]
{{
background-color:40,50,80;
}}
[data-baseweb="base-input"]
{{
background-color:transparent;
}}
[id="text_input_1"]
{{
background-color:transparent;
}}
h1{{
color: rgba(232, 193, 255, 0.97);
}}
header{{
color: rgba(244, 223, 249, 0.97);;
}}
[data-testid="stMarkdownContainer"]
{{
color: rgb(255, 144, 184);
}}
[data-testid="baseButton-secondary"]
{{
background-color: rgba(27, 1, 42, 0.97);

}}
[data-testid="stSidebarContent"]
{{
background-image: url("data:side02/jpg;base64,{img01}");
background-position:center;
}}

</style>
"""
st.markdown(page_by_img, unsafe_allow_html=True)



st.sidebar.title("Navigation")
option = st.sidebar.radio("Choose a functionality:", ["Medical Chatbot", "Image Query", "Document Summary"])

st.header("Medical Application")

if option == "Medical Chatbot":
    st.subheader("Medical Chatbot")
    input_text = st.text_input("Enter your question here:", key="text_input")
    submit_text = st.button("Submit")

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