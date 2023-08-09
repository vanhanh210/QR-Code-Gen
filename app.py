import streamlit as st
from PIL import Image
import qrcode
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

    # Generate the QR code
    qr = qrcode.QRCode(
        version=6,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=6,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill='black', back_color='white').convert('RGB')

    # Place logo in the center if uploaded
    if logo_file:
        logo = Image.open(logo_file)
        logo = logo.convert("RGBA")
        logo_size = 100 # Adjust logo size
        logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)
        logo_w, logo_h = logo.size
        qr_img_w, qr_img_h = qr_img.size
        offset = ((qr_img_w - logo_w) // 2, (qr_img_h - logo_h) // 2)
        qr_img.paste(logo, offset, logo) # logo as the mask parameter to handle transparency

    # Save the image to a BytesIO object
    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)

    # Display the image
    st.image(buffer, caption='Generated QR Code', use_column_width=True)
