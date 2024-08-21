import streamlit as st
from PIL import Image
import io

# HTML to capture image from the camera
st.markdown(
    """
    <input type="file" accept="image/*" capture="camera" id="cameraInput">
    <br>
    <img id="cameraImage" src="" alt="Captured Image" width="300">
    <script>
    document.getElementById('cameraInput').addEventListener('change', function(e) {
        var reader = new FileReader();
        reader.onload = function(event) {
            document.getElementById('cameraImage').src = event.target.result;
        }
        reader.readAsDataURL(e.target.files[0]);
    });
    </script>
    """,
    unsafe_allow_html=True
)

# Image upload functionality
uploaded_file = st.file_uploader("Upload an image")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
