import streamlit as st
from PIL import Image
import os
from RSAEncryption import enc

def app():
    st.title('Image Upload for Payment Gateway')

    def save_uploaded_file(directory, file):
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = os.path.join(directory, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        return file_path

    def show_data(image_path):
        # Assuming a context is managed appropriately elsewhere if needed
        return enc(image_path=image_path)

    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        file_path = save_uploaded_file("uploaded_images", uploaded_file)
        image = Image.open(file_path)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        st.success("Image uploaded successfully")

        if st.button("Show Data"):
            data = show_data(file_path)
            st.text_input("Card Number", value=data[0])
            st.text_input("Card Number Encrypted", value=data[4])
            st.text_input("Expiry Date", value=data[1])
            st.text_input("Expiry Date Encrypted", value=data[5])
            st.text_input("Type of Card", value=data[2])
            st.text_input("Type of Card Encrypted", value=data[6])
            st.text_input("Account Holder's Name", value=data[3])
            st.text_input("Account Holder's Name Encrypted", value=data[7])
