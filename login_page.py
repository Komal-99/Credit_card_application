import streamlit as st
from authenticate import login, register
from dashboard import main_app

def main():
    st.title('Welcome to Credit Card Application')

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['navigation'] = 'Login'  # Default to login page

    if st.session_state['logged_in']:
        # Redirects to the main app/dashboard
        main_app()
    else:
        choice = st.sidebar.selectbox('Login/Signup', ['Login', 'Register'])
        handle_auth(choice)
def handle_auth(choice):
    if choice == 'Login':
        username = st.text_input('Email')
        password = st.text_input('Password', type="password")
        if st.button('Login'):
            if login(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.rerun()
            else:
                st.error('Incorrect username or password')
    elif choice == 'Register':
        # Registration logic here
        with st.form("Register"):
            name = st.text_input('Name')
            age = st.number_input('Age', min_value=18, max_value=100, step=1)
            email = st.text_input('Email')
            city = st.text_input('City')
            card_type = st.selectbox('Card Type', ['Debit', 'Credit'])
            credit_limit = st.number_input('Credit Limit', min_value=1000, max_value=100000, step=100)
            company = st.text_input('Company')
            job_segment = st.text_input('Job Segment')
            password = st.text_input('Password', type="password")
            submitted = st.form_submit_button("Register")
            if submitted:
                register(name, age, email, city, card_type, credit_limit, company, job_segment,password)
                # st.success('Registered successfully. Please go to the Login tab to login.')

                st.success('Registered successfully. Please log in.')
                st.session_state['navigation'] = 'Login'  # Change navigation to login
                st.rerun()

if __name__ == "__main__":
    main()
