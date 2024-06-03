import streamlit as st
from pages import upload_function, chatbot

PAGES = {
    "Image Upload": upload_function,
    "Chatbot": chatbot
}

def main_app():
    st.sidebar.title('Navigation')
    # Logout button in the sidebar
    if st.sidebar.button('Logout'):
        st.session_state['logged_in'] = False
        st.session_state.pop('username', None)  # Optionally clear the username
        st.experimental_rerun()  # Rerun the app to update the state

    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()
