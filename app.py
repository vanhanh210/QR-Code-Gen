import streamlit as st
import qrcode
from PIL import Image
import io
import pyshorteners

st.title('QR Code Generator')

# Option to use shortlink
shorten_url = st.sidebar.checkbox('Use shortlink (TinyURL)?')

# Input for the user to enter the URL
url = st.text_input('Enter the URL you want to convert to QR Code:')

if url and shorten_url:
    # Shorten the URL using TinyURL
    s = pyshorteners.Shortener()
    url = s.tinyurl.short(url)
    st.write('Shortened URL:', url)

if url:
    # Create a QR Code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add the URL
    qr.add_data(url)
    qr.make(fit=True)

    # Create an Image object from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a BytesIO object
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Display the image
    st.image(buffer, caption='Generated QR Code', use_column_width=True)
