import cv2
import numpy as np
from pyzbar.pyzbar import decode
import easyocr
import streamlit as st

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Initialize session state
if 'detected_barcodes' not in st.session_state:
    st.session_state.detected_barcodes = set()
if 'barcode_data_list' not in st.session_state:
    st.session_state.barcode_data_list = []
if 'ocr_text' not in st.session_state:
    st.session_state.ocr_text = None
if 'captured_frame' not in st.session_state:
    st.session_state.captured_frame = None

def extract_required_number(text):
    if isinstance(text, str):
        return text[-7:] if len(text) >= 7 else text
    else:
        return None

def capture_and_detect_barcodes():
    st.header("Step 1: Capture and Detect Barcodes (ステップ1: バーコードを検出する)")
    st.write("Capture two different barcodes before proceeding to OCR. (OCRに進む前に、2つの異なるバーコードを検出してください。)")

    try:
        # Use Streamlit's camera_input() to capture the image
        camera = st.camera_input("Camera")
        if camera is not None:
            st.session_state.captured_frame = np.array(camera)

            # Decode barcodes in the frame
            barcodes = decode(st.session_state.captured_frame)

            for barcode in barcodes:
                barcode_data = barcode.data.decode('utf-8')
                barcode_type = barcode.type

                if barcode_data not in st.session_state.detected_barcodes:
                    st.session_state.detected_barcodes.add(barcode_data)
                    st.session_state.barcode_data_list.append(barcode_data)
                    st.write(f"Detected barcode: {barcode_data}, Type: {barcode_type}")

                    if len(st.session_state.barcode_data_list) == 1:
                        st.write("First barcode detected. Looking for the second barcode...(最初のバーコードが検出されました。次のバーコードを探しています...)")
                    elif len(st.session_state.barcode_data_list) == 2:
                        st.write("Second barcode detected. Proceeding to OCR...(2番目のバーコードが検出されました。OCRに進行します...)")
                        break
    except Exception as e:
        st.error(f"An error occurred: {e}")

def capture_and_perform_ocr():
    st.header("Step 2: Capture Image and Perform OCR (ステップ2: 画像をキャプチャしてOCRを実行する)")
    st.write("Click the button below to capture the image and perform OCR.(下のボタンをクリックして画像をキャプチャしてOCRを実行してください。)")
    
    try:
        # Use Streamlit's camera_input() to capture the image
        camera = st.camera_input("Camera")
        if camera is not None:
            st.write("Capturing image and performing OCR...(画像をキャプチャしてOCRを実行しています...)")
            st.session_state.captured_frame = np.array(camera)

            # Perform OCR on the captured image
            results = reader.readtext(st.session_state.captured_frame, allowlist='0123456789')
            
            ocr_texts = []
            # Draw bounding boxes around detected text and display the text
            for (bbox, text, prob) in results:
                (top_left, top_right, bottom_right, bottom_left) = bbox
                top_left = tuple(map(int, top_left))
                bottom_right = tuple(map(int, bottom_right))
                cv2.rectangle(st.session_state.captured_frame, top_left, bottom_right, (0, 255, 0), 2)
                cv2.putText(st.session_state.captured_frame, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                ocr_texts.append(text)
            
            st.image(st.session_state.captured_frame, channels="BGR", caption="OCR Results (OCR結果)")

            # Extract the required number from the OCR results
            required_number = extract_required_number(ocr_texts[-1])
            st.session_state.ocr_text = required_number
            st.write(f"OCR Number: {required_number}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def compare_results():
    st.header("Step 3: Compare Results (ステップ3: 結果を比較する)")

    if len(st.session_state.barcode_data_list) >= 2 and st.session_state.ocr_text is not None:
        barcode1 = st.session_state.barcode_data_list[0][-7:]
        barcode2 = st.session_state.barcode_data_list[1][-7:]
        ocr_number = st.session_state.ocr_text

        st.write(f"Barcode 1: {barcode1}")
        st.write(f"Barcode 2: {barcode2}")
        st.write(f"OCR Number: {ocr_number}")

        if barcode1 == barcode2 == ocr_number:
            st.success("""The numbers from barcode1, barcode2, and OCR match!
            (バーコード1、バーコード2、そしてOCRの数字が一致しました！)""")
        else:
            st.error("""The numbers do not match. 
            (数字が一致しません。)""")
    else:
        st.warning("""Not enough information to compare.
        (比較するための情報が十分ではありません。)""")

# Streamlit app layout
capture_and_detect_barcodes()
capture_and_perform_ocr()
compare_results()