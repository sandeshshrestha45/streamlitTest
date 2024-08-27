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

    # Capture first image
    st.write("Click the button to capture the first image.")
    img_file1 = st.camera_input("Capture First Image")
    
    if img_file1:
        # Load the first image file
        image1 = Image.open(img_file1)
        image1_np = np.array(image1)
        st.image(image1, caption='Captured Image 1', use_column_width=True)
        
        # Perform barcode detection on the first image
        barcode_info1 = detect_barcode(image1_np)
        
        if barcode_info1:
            st.write("Detected Barcode Information for Image 1:")
            for info in barcode_info1:
                st.write(info)
        else:
            st.write("No barcode detected in Image 1.")
        
                
        # Capture second image
        st.write("Click the button to capture the second image.")
        img_file2 = st.camera_input("Capture Second Image")
        
        if img_file2:
            # Load the second image file
            image2 = Image.open(img_file2)
            image2_np = np.array(image2)
            st.image(image2, caption='Captured Image 2', use_column_width=True)
            
            # Perform barcode detection on the second image
            barcode_info2 = detect_barcode(image2_np)
            
            if barcode_info2:
                st.write("Detected Barcode Information for Image 2:")
                for info in barcode_info2:
                    st.write(info)
            else:
                st.write("No barcode detected in Image 2.")
            
           
if __name__ == "__main__":
    main()
