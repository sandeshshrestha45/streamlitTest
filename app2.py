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
if 'captured_frame' not in st.session_state:
    st.session_state.captured_frame = None
if 'capture_started' not in st.session_state:
    st.session_state.capture_started = False
if 'ocr_performed' not in st.session_state:
    st.session_state.ocr_performed = False

def extract_required_number(text):
    return text[-7:] if len(text) >= 7 else text

def display_video_feed():
    st.header("Step 1: Detect Barcodes (ステップ1: バーコードを検出する)")
    st.write("Detect two different barcodes before proceeding to OCR. (OCRに進む前に、2つの異なるバーコードを検出してください。)")

    try:
        # Use Streamlit's camera_input() instead of cv2.VideoCapture()
        camera = st.camera_input("Camera")
        if camera is not None:
            frame = np.array(camera)

            # Decode barcodes in the frame
            barcodes = decode(frame)

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
                        st.write("Second barcode detected. Stopping the video stream now. (2番目のバーコードが検出されました。これからビデオストリームを停止します。)")
                        break
    except Exception as e:
        st.error(f"An error occurred: {e}")

def capture_image_for_ocr():
    st.header("Step 2: Capture Image for OCR (ステップ2: OCRのために画像をキャプチャする)")
    st.write("Click the button below to capture the image.(下のボタンをクリックして画像をキャプチャしてください。)")
    
    try:
        # Use Streamlit's camera_input() to capture the image
        camera = st.camera_input("Camera")
        if camera is not None:
            st.write("Capturing image...(画像をキャプチャ中...)")
            st.session_state.captured_frame = np.array(camera)
            st.write("Image captured. Proceeding to OCR...(画像がキャプチャされました。OCRに進行します...)")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def process_ocr():
    st.header("Step 3: OCR Processing (ステップ3: OCR処理)")
    st.write("Performing OCR on the captured image. (キャプチャされた画像でOCRを実行しています。)")
    
    if st.session_state.captured_frame is not None:
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
        required_numbers = [extract_required_number(text) for text in ocr_texts]

        # Check if the barcode data matches the OCR number
        if len(st.session_state.barcode_data_list) >= 2 and required_numbers:
            barcode1 = st.session_state.barcode_data_list[0][-7:]
            barcode2 = st.session_state.barcode_data_list[1][-7:]
            ocr_number = required_numbers[-1][-7:]

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
            st.warning("""Not enough barcodes or OCR data to compare.
            (比較するためのバーコードやOCRデータが十分ではありません。)""")
    else:
        st.error("""No image was captured for OCR processing.
        (OCR処理のための画像がキャプチャされませんでした。)""")

# Streamlit app layout
if len(st.session_state.barcode_data_list) < 2:
    display_video_feed()

if len(st.session_state.barcode_data_list) == 2 and st.session_state.captured_frame is None:
    capture_image_for_ocr()

if st.session_state.captured_frame is not None:
    process_ocr()