import streamlit as st
from authenticate import login, register
from dashboard import main_app
def main():
    st.title('Welcome to Credit Card Application')
    st.sidebar.title("Navigation")
    choice = st.sidebar.selectbox('Login/Signup', ['Login', 'Register'])

    # Initialize logged_in status in the session state if not already present
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Show Logout button if user is logged in
    if st.session_state['logged_in']:
        if st.sidebar.button('Logout'):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None  # Clear the username from session state
            st.sidebar.success("You have been logged out.")
            st.experimental_rerun()  # Rerun the app to refresh the state

    # Handle login and registration choices
    if choice == 'Login':
        if st.session_state['logged_in']:
            st.sidebar.success('Already logged in as {}'.format(st.session_state['username']))
            main_app()  # Redirects to the main app/dashboard
        else:
            username = st.sidebar.text_input('Email')
            password = st.sidebar.text_input('Password', type="password")
            if st.sidebar.button('Login'):
                if login(username, password):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.sidebar.success('Logged in as {}'.format(username))
                    main_app()  # Redirects to the main app/dashboard
                else:
                    st.sidebar.error('Incorrect username or password')

    elif choice == 'Register':
        with st.sidebar.form("Register"):
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
                st.sidebar.success('Registered successfully. Please go to the Login tab to login.')

if __name__ == "__main__":
    main()
