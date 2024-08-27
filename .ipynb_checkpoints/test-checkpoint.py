import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("Enhanced Camera Input with OpenCV")

# Capture image from camera
img = st.camera_input("Capture Image")

if img:
    # Convert to OpenCV format
    image = Image.open(img)
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Resize image to simulate higher resolution
    new_size = (image_cv.shape[1] * 2, image_cv.shape[0] * 2)  # Double the resolution
    resized_image = cv2.resize(image_cv, new_size, interpolation=cv2.INTER_CUBIC)

    # Convert back to PIL for displaying
    enhanced_image = Image.fromarray(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
    print(image_np.shape)

    st.image(enhanced_image, caption="Enhanced Image", use_column_width=True)
