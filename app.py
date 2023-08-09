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

# Upload logo
logo_file = st.file_uploader('Upload your logo (optional):')

if url:
    if shorten_url:
        # Shorten the URL using TinyURL
        s = pyshorteners.Shortener()
        url = s.tinyurl.short(url)
        st.write('Shortened URL:', url)

    # Create a QR Code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    # Add the URL
    qr.add_data(url)
    qr.make(fit=True)

    # Create an Image object from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # Add the logo if uploaded
    if logo_file:
        logo = Image.open(logo_file)
        logo = logo.resize((50, 50))  # Adjust size to fit inside QR code
        img_w, img_h = img.size
        logo_w, logo_h = logo.size
        offset = ((img_w - logo_w) // 2, (img_h - logo_h) // 2)
        img.paste(logo, offset)

    # Save the image to a BytesIO object
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Display the image
    st.image(buffer, caption='Generated QR Code', use_column_width=True)
