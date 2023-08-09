import streamlit as st
import qrcode
from qrcode.image.pil import PilImage
from PIL import Image, ImageDraw
import io
import base64

st.title('QR Code Generator with Custom Style')

# Option to use shortlink
shorten_url = st.sidebar.checkbox('Use shortlink (TinyURL)?')

# Input for the user to enter the URL
url = st.text_input('Enter the URL you want to convert to QR Code:')

# Options to select quality, format, version, shape, and colors
quality = st.sidebar.slider('Select Quality (DPI):', min_value=72, max_value=300, value=150, step=1)
format_options = st.sidebar.selectbox('Select Image Format:', options=['PNG', 'JPEG', 'BMP'])
format_extension = format_options.lower()
version_options = st.sidebar.slider('Select QR Code Version (1-40):', min_value=1, max_value=40, value=6, step=1)
shape_options = st.sidebar.selectbox('Select Shape:', options=['Square', 'Circle'])
fill_color_options = st.sidebar.color_picker('Select Fill Color:', value='#000000')
back_color_options = st.sidebar.color_picker('Select Background Color:', value='#FFFFFF')

if url:
    # Create a QR Code instance with selected version
    qr = qrcode.QRCode(
        version=version_options,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )
    
    # Add the URL
    qr.add_data(url)
    qr.make(fit=True)

    # Create an Image object from the QR Code instance
    img = qr.make_image(fill_color=fill_color_options, back_color=back_color_options, image_factory=PilImage).convert('RGB')

    # If shape is Circle, modify the QR code modules to be circular
    if shape_options == 'Circle':
        img_pixels = img.load()
        for r in range(img.size[0]):
            for c in range(img.size[1]):
                if img_pixels[r, c] == (0, 0, 0):  # If the pixel is part of a QR code module
                    draw = ImageDraw.Draw(img)
                    draw.ellipse([r, c, r + 10, c + 10], fill=fill_color_options)

    # Save the image to a BytesIO object
    buffer = io.BytesIO()
    img.save(buffer, format=format_extension, dpi=(quality, quality))
    buffer.seek(0)

    # Display the image
    st.image(buffer, caption='Generated QR Code', use_column_width=True)

    # Decorated Download Button
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    download_button = f'<a href="data:image/{format_extension};base64,{b64}" download="qr_code.{format_extension}" style="display: inline-block; padding: .5rem 1rem; border: 1px solid #ccc; border-radius: .25rem; background-color: #f8f9fa; text-decoration: none; color: #495057;">Download QR Code</a>'
    st.markdown(download_button, unsafe_allow_html=True)

# Donate Button in Footer
st.markdown(
    """
    <div style="position: fixed; bottom: 10px; right: 10px; padding: 10px; background-color: #f9f9f9; border: 1px solid #ccc; border-radius: 10px;">
        <span>Buy Vanh coffee: VpBank 200166302</span>
    </div>
    """,
    unsafe_allow_html=True,
)
