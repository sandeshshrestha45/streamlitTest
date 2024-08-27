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
    ocr_text = [result[1] for result in results if len(result[1]) >= 4]
    return ocr_text

def main():
    st.title("シンワアクティブ SHINWA ACTIVE")

    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'ocr_results' not in st.session_state:
        st.session_state.ocr_results = []

    if st.session_state.step <= 3:
        st.write(f"Step {st.session_state.step}: 「画像をキャプチャしてください」Capture Image {st.session_state.step}")
        img_file = st.camera_input(f"「画像をキャプチャしてください」Capture Image {st.session_state.step}")
        
        if img_file:
            # Load and upscale the image
            image = Image.open(img_file)
            image_np = np.array(image)
            upscaled_image = upscale_image(image_np)
            st.image(image, caption=f'キャプチャされた画像 Captured Image {st.session_state.step}', use_column_width=True)
            
            # Perform OCR on the upscaled image
            ocr_text = perform_ocr(upscaled_image)
            
            if ocr_text:
                st.write(f"画像から抽出された数字 Extracted Numbers from Image {st.session_state.step}:")
                st.write(ocr_text)
                st.session_state.ocr_results.append(ocr_text)
            else:
                st.write(f"画像に数字が検出されませんでした No numbers detected in Image {st.session_state.step}.")
                st.session_state.ocr_results.append([])
            
            # st.write(f"Original Image {st.session_state.step} shape: {image_np.shape}")
            # st.write(f"Upscaled Image {st.session_state.step} shape: {upscaled_image.shape}")
            
            # Move to the next step
            st.session_state.step += 1
            if st.session_state.step <= 3:
                st.rerun()

    # Compare OCR results after all images are captured
    if len(st.session_state.ocr_results) == 3:
        st.write("OCR結果の比較 Comparison of OCR results:")
        
        # Get the first element of the first and second OCR results, or 'N/A' if the list is empty
        results = [ocr[0] if ocr else 'N/A' for ocr in st.session_state.ocr_results[:2]]
        
        # Add the second last element of the third OCR result
        if len(st.session_state.ocr_results[2]) >= 2:
            results.append(st.session_state.ocr_results[2][1][-7:])
        else:
            results.append('N/A')

        # Check if all results match
        all_match = len(set(results)) == 1 and 'N/A' not in results
        
        for i, result in enumerate(results, 1):
            if all_match:
                st.markdown(f"OCR結果 OCR result {i}: <font color='green'>{result}</font>", unsafe_allow_html=True)
            else:
                st.markdown(f"OCR結果 OCR result {i}: <font color='red'>{result}</font>", unsafe_allow_html=True)
        
        if all_match:
            st.success("すべての画像のOCR結果が一致しました！The OCR results from all images match!")
        else:
            st.error("OCRの結果が一致しません。The OCR results do not match.")
        
        # Button to start over
        if st.button("最初からやり直してください。Start Over"):
            st.session_state.step = 1
            st.session_state.ocr_results = []
            st.rerun()

if __name__ == "__main__":
    main()
