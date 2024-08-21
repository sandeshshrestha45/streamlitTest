import streamlit as st
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import io
import easyocr

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

def perform_ocr(image):
    """Perform OCR on the image and return the extracted text."""
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image)
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
        st.write(image1_np.shape)
        
        # Perform barcode detection on the first image
        barcode_info1 = detect_barcode(image1_np)
        
        if barcode_info1:
            st.write("Detected Barcode Information for Image 1:")
            for info in barcode_info1:
                st.write(info)
        else:
            st.write("No barcode detected in Image 1.")
        
        # Save barcode information for the first image
        # with open('barcode_info1.txt', 'w') as f:
        #     for info in barcode_info1:
        #         f.write(info + '\n')

        # st.write("Barcode information for Image 1 saved to 'barcode_info1.txt'.")
        
        # Capture second image
        st.write("Click the button to capture the second image.")
        img_file2 = st.camera_input("Capture Second Image")
        
        if img_file2:
            # Load the second image file
            image2 = Image.open(img_file2)
            image2_np = np.array(image2)
            st.image(image2, caption='Captured Image 2', use_column_width=True)

            st.write(image2_np.shape)

            # Perform barcode detection on the second image
            barcode_info2 = detect_barcode(image2_np)
            
            if barcode_info2:
                st.write("Detected Barcode Information for Image 2:")
                for info in barcode_info2:
                    st.write(info)
            else:
                st.write("No barcode detected in Image 2.")
            
            # # Save barcode information for the second image
            # with open('barcode_info2.txt', 'w') as f:
            #     for info in barcode_info2:
            #         f.write(info + '\n')

            # st.write("Barcode information for Image 2 saved to 'barcode_info2.txt'.")
        
            # Capture third image
            st.write("Click the button to capture the third image.")
            img_file3 = st.camera_input("Capture Third Image")
            
            if img_file3:
                # Load the third image file
                image3 = Image.open(img_file3)
                image3_np = np.array(image3)
                st.image(image3, caption='Captured Image 3', use_column_width=True)

                st.write(image1_np.shape)
                
                # Perform OCR on the third image
                ocr_text = perform_ocr(image3_np)
                
                if ocr_text:
                    st.write("Extracted Text from Image 3:")
                    for text in ocr_text:
                        st.write(text)
                else:
                    st.write("No text detected in Image 3.")
                
                # Save OCR information for the third image
                # with open('ocr_info3.txt', 'w') as f:
                #     for text in ocr_text:
                #         f.write(text + '\n')

                # st.write("OCR information for Image 3 saved to 'ocr_info3.txt'.")

if __name__ == "__main__":
    main()
