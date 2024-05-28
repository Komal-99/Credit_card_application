import streamlit as st
from pages import upload_function, chatbot

PAGES = {
    "Image Upload": upload_function,
    "Chatbot": chatbot
}

def main_app():
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]
    page.app()

