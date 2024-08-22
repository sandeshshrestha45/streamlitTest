import streamlit as st
import cv2
import numpy as np
from PIL import Image
import easyocr

def upscale_image(image, scale_factor=2):
    """Upscale the image by the given scale factor."""
    height, width = image.shape[:2]
    new_height, new_width = int(height * scale_factor), int(width * scale_factor)
    return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

def perform_ocr(image):
    """Perform OCR on the upscaled image and return the extracted text."""
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image, allowlist='0123456789')
    ocr_text = [result[1] for result in results]
    return ocr_text

def main():
    st.title("Image Processing App")

    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'ocr_results' not in st.session_state:
        st.session_state.ocr_results = []

    if st.session_state.step <= 3:
        st.write(f"Step {st.session_state.step}: Capture Image {st.session_state.step}")
        img_file = st.camera_input(f"Capture Image {st.session_state.step}")
        
        if img_file:
            # Load and upscale the image
            image = Image.open(img_file)
            image_np = np.array(image)
            upscaled_image = upscale_image(image_np)
            st.image(image, caption=f'Captured Image {st.session_state.step}', use_column_width=True)
            
            # Perform OCR on the upscaled image
            ocr_text = perform_ocr(upscaled_image)
            
            if ocr_text:
                st.write(f"Extracted Numbers from Image {st.session_state.step}:")
                st.write(ocr_text)
                st.session_state.ocr_results.append(ocr_text)
            else:
                st.write(f"No numbers detected in Image {st.session_state.step}.")
                st.session_state.ocr_results.append([])
            
            st.write(f"Original Image {st.session_state.step} shape: {image_np.shape}")
            st.write(f"Upscaled Image {st.session_state.step} shape: {upscaled_image.shape}")
            
            # Move to the next step
            st.session_state.step += 1
            if st.session_state.step <= 3:
                st.rerun()

    # Compare OCR results after all images are captured
    if len(st.session_state.ocr_results) == 3:
        st.write("Comparison of OCR results:")
        
        # Get the first element of each OCR result list, or 'N/A' if the list is empty
        results = [ocr[0] if ocr else 'N/A' for ocr in st.session_state.ocr_results]
        
        # Check if all results match
        all_match = len(set(results)) == 1 and 'N/A' not in results
        
        for i, result in enumerate(results, 1):
            if all_match:
                st.markdown(f"Image {i} OCR result: <font color='green'>{result}</font>", unsafe_allow_html=True)
            else:
                st.markdown(f"Image {i} OCR result: <font color='red'>{result}</font>", unsafe_allow_html=True)
        
        if all_match:
            st.success("The OCR results from all three images match!")
        else:
            st.error("The OCR results from the three images do not match.")
        
        # Button to start over
        if st.button("Start Over"):
            st.session_state.step = 1
            st.session_state.ocr_results = []
            st.rerun()

if __name__ == "__main__":
    main()

