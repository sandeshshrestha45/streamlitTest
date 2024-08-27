import streamlit as st
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image

# Define a function to detect barcodes
def detect_barcode(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray)
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        barcode_data = barcode.data.decode('utf-8')
        cv2.putText(image, barcode_data, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image

# Create a Streamlit app
st.title("Barcode Detection from Camera")

# Open a camera input stream
img_file = st.camera_input("Capture an Image")

if img_file:
    # Convert the captured image to an OpenCV-compatible format
    image = Image.open(img_file)
    image = np.array(image)

    # Detect barcodes in the image
    image_with_barcodes = detect_barcode(image)

    # Convert the frame to an image for Streamlit display
    st.image(image_with_barcodes, channels="BGR")
