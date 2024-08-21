import streamlit as st
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import io
import easyocr

def upscale_image(image, scale_factor=2):
    """Upscale the image by the given scale factor."""
    height, width = image.shape[:2]
    new_height, new_width = int(height * scale_factor), int(width * scale_factor)
    return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

def detect_barcode(image):
    """Detect barcodes in the image and return the decoded information."""
    # Upscale the image
    upscaled_image = upscale_image(image)
    
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(upscaled_image, cv2.COLOR_BGR2GRAY)
    
    # Decode barcodes
    barcodes = decode(gray_image)
    barcode_info = []
    
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        barcode_info.append(barcode_data)
    
    return barcode_info

def perform_ocr(image):
    """Perform OCR on the image and return the extracted text."""
    # Upscale the image
    upscaled_image = upscale_image(image)
    
    reader = easyocr.Reader(['en'])
    results = reader.readtext(upscaled_image)
    ocr_text = [result[1] for result in results]
    return ocr_text

def main():
    st.title("Image Processing App")

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
        
        st.write(f"Original Image 1 shape: {image1_np.shape}")
        st.write(f"Upscaled Image 1 shape: {upscale_image(image1_np).shape}")

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
            
            st.write(f"Original Image 2 shape: {image2_np.shape}")
            st.write(f"Upscaled Image 2 shape: {upscale_image(image2_np).shape}")
            
            # Capture third image
            st.write("Click the button to capture the third image.")
            img_file3 = st.camera_input("Capture Third Image")
            
            if img_file3:
                # Load the third image file
                image3 = Image.open(img_file3)
                image3_np = np.array(image3)
                st.image(image3, caption='Captured Image 3', use_column_width=True)
                
                # Perform OCR on the third image
                ocr_text = perform_ocr(image3_np)
                
                if ocr_text:
                    st.write("Extracted Text from Image 3:")
                    for text in ocr_text:
                        st.write(text)
                else:
                    st.write("No text detected in Image 3.")
                
                st.write(f"Original Image 3 shape: {image3_np.shape}")
                st.write(f"Upscaled Image 3 shape: {upscale_image(image3_np).shape}")

                # Compare barcode information and OCR text
                if len(barcode_info1) > 0 and len(barcode_info2) > 0 and len(ocr_text) > 0:
                    barcode1 = barcode_info1[0][-7:]
                    barcode2 = barcode_info2[0][-7:]
                    ocr_number = ''.join(filter(str.isdigit, ocr_text[-1]))[-7:]

                    st.write(f"Barcode 1: {barcode1}")
                    st.write(f"Barcode 2: {barcode2}")
                    st.write(f"OCR Number: {ocr_number}")

                    if barcode1 == barcode2 == ocr_number:
                        st.success("The numbers from barcode1, barcode2, and OCR match!")
                    else:
                        st.error("The numbers do not match.")
                else:
                    st.warning("Not enough information to compare barcodes and OCR text.")

if __name__ == "__main__":
    main()