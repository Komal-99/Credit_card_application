import streamlit as st
import requests

def app():
    st.title('Chatbot')

    # Custom CSS for message styling
    st.markdown(
        """
        <style>
            .message {
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
                color: black; 
            }
            .user {
                border: 1px solid #4CAF50;
                background-color: #DFF0D8;
                text-align: right;
                float: right;
                clear: both;
                width: 60%;
            }
            .bot {
                border: 1px solid #FF5722;
                background-color: #FDE0DC;
                text-align: left;
                float: left;
                clear: both;
                width: 60%;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'clear_input' not in st.session_state:
        st.session_state.clear_input = False

    # Clear the input if required
    user_input = st.text_input("Ask me anything...", value="" if st.session_state.clear_input else None, key="user_input")

    if st.button("Send"):
        if user_input:
            response = requests.post("http://localhost:5000/credit_bot", json={"ques": user_input})
            if response.status_code == 200:
                answer = response.json().get("answer", "No response from API")
                st.session_state.chat_history.append({"role": "user", "message": user_input})
                st.session_state.chat_history.append({"role": "bot", "message": answer})
            else:
                st.session_state.chat_history.append({"role": "bot", "message": "Error connecting to bot server"})
            st.session_state.clear_input = True
        else:
            st.session_state.clear_input = False

    # Display chat history
    for chat in st.session_state.chat_history:
        if chat['role'] == 'user':
            st.markdown(f"<div class='message user'>{chat['message']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='message bot'>{chat['message']}</div>", unsafe_allow_html=True)

    # Reset the flag to clear the text input for the next input
    if st.session_state.clear_input:
        st.session_state.clear_input = False
