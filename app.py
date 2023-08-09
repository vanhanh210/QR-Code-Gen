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
        version=6,  # Choose an appropriate version to fit the logo
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    # Add the URL
    qr.add_data(url)
    qr.make(fit=True)

    # Create an Image object from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    img_w, img_h = img.size

    # Create a blank space for the logo if uploaded
    if logo_file:
        logo_size = 50  # Adjust as needed
        offset = ((img_w - logo_size) // 2, (img_h - logo_size) // 2)
        for y in range(offset[1], offset[1] + logo_size):
            for x in range(offset[0], offset[0] + logo_size):
                img.putpixel((x, y), (255, 255, 255))

        logo = Image.open(logo_file)
        logo = logo.resize((logo_size, logo_size))  # Adjust size to fit inside QR code
        img.paste(logo, offset)

    # Save the image to a BytesIO object
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Display the image
    st.image(buffer, caption='Generated QR Code', use_column_width=True)
