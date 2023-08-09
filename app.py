import streamlit as st
import qrcode
from PIL import Image, ImageDraw
import io
import pyshorteners
import base64

def draw_module(draw, shape, x, y, size, fill_color):
    if shape == 'Rounded':
        draw.rectangle([x, y, x + size, y + size], outline=fill_color, width=1)
        draw.ellipse([x, y, x + size, y + size], fill=fill_color)
    elif shape == 'Dot':
        draw.ellipse([x, y, x + size, y + size], fill=fill_color)
    elif shape == 'Small-Rounded':
        draw.rectangle([x, y, x + size, y + size], fill=fill_color)
        draw.ellipse([x + 2, y + 2, x + size - 2, y + size - 2], fill='white')
    elif shape == 'Large-Circles-Dash':
        draw.ellipse([x + 2, y + 2, x + size - 2, y + size - 2], outline=fill_color, width=2)
    else:  # Square
        draw.rectangle([x, y, x + size, y + size], fill=fill_color)

st.title('QR Code Generator with Logo')

# Option to use shortlink
shorten_url = st.sidebar.checkbox('Use shortlink (TinyURL)?')

# Input for the user to enter the URL
url = st.text_input('Enter the URL you want to convert to QR Code:')

# Option to upload a logo
uploaded_logo = st.file_uploader('Upload a logo (optional):')

# Options to select quality, format, and version
quality = st.sidebar.slider('Select Quality (DPI):', min_value=72, max_value=300, value=150, step=1)
format_options = st.sidebar.selectbox('Select Image Format:', options=['PNG', 'JPEG', 'BMP'])
format_extension = format_options.lower()
version_options = st.sidebar.slider('Select QR Code Version (1-40):', min_value=1, max_value=40, value=6, step=1)

if url and shorten_url:
    # Shorten the URL using TinyURL
    s = pyshorteners.Shortener()
    url = s.tinyurl.short(url)
    st.write('Shortened URL:', url)

shape_options = st.sidebar.selectbox('Select Shape:', options=['Square', 'Rounded', 'Dot', 'Small-Rounded', 'Large-Circles-Dash'])
fill_color_options = st.sidebar.color_picker('Select Fill Color:', value='#000000')

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
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')


    # Customize the shape of the modules
    draw = ImageDraw.Draw(img)
    for r in range(qr.modules_count):
        for c in range(qr.modules_count):
            if qr.modules[r][c]:
                draw_module(draw, shape_options, r * 10, c * 10, 10, fill_color_options)
                
    # If a logo is uploaded, embed it in the center of the QR code
    if uploaded_logo:
        logo = Image.open(uploaded_logo).convert('RGBA')
        logo_size = 80
        logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)
        qr_size = img.size[0]
        logo_position = ((qr_size - logo_size) // 2, (qr_size - logo_size) // 2)

        # Create a white box in the center of QR code where the logo will be placed
        for x in range(logo_position[0], logo_position[0] + logo_size):
            for y in range(logo_position[1], logo_position[1] + logo_size):
                img.putpixel((x, y), (255, 255, 255))

        # Paste the logo
        img.paste(logo, logo_position, mask=logo)

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