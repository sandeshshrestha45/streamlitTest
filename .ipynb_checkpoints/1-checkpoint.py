import streamlit as st
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import io

def detect_barcode(image):
    """Detect barcodes in the image and return the decoded information."""
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Decode barcodes
    barcodes = decode(gray_image)
    barcode_info = []
    
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        barcode_info.append(barcode_data)
    
    return barcode_info

def main():
    st.title("Barcode Detection App")

    # Capture image using Streamlit
    st.write("Click the button to capture an image.")
    img_file = st.camera_input("Capture Image")
    
    if img_file:
        # Load image file
        image = Image.open(img_file)
        image_np = np.array(image)

        st.image(image, caption='Captured Image', use_column_width=True)
        
        # Perform barcode detection
        barcode_info = detect_barcode(image_np)
        
        if barcode_info:
            st.write("Detected Barcode Information:")
            for info in barcode_info:
                st.write(info)
            
        else:
            st.write("No barcode detected.")

if __name__ == "__main__":
    main()
