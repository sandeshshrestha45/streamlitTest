import streamlit as st
import cv2
import numpy as np
from PIL import Image
import easyocr
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import pytz
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
# Now access the environment variables
project_id = os.getenv('GCP_PROJECT_ID')
private_key_id = os.getenv('GCP_PRIVATE_KEY_ID')
private_key = os.getenv('GCP_PRIVATE_KEY')
client_email = os.getenv('GCP_CLIENT_EMAIL')
client_id = os.getenv('GCP_CLIENT_ID')
client_x509_cert_url = os.getenv('GCP_CLIENT_X509_CERT_URL')
# print(os.getenv('GCP_PROJECT_ID'))
# print(os.getenv('GCP_PRIVATE_KEY_ID'))
# print(os.getenv('GCP_PRIVATE_KEY'))
# print(os.getenv('GCP_CLIENT_EMAIL'))
# print(os.getenv('GCP_CLIENT_ID'))
# print(os.getenv('GCP_CLIENT_X509_CERT_URL'))


def upscale_image(image, scale_factor=2):
    height, width = image.shape[:2]
    new_height, new_width = int(height * scale_factor), int(width * scale_factor)
    return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

def perform_ocr(image):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image, allowlist='0123456789')
    ocr_text = [result[1] for result in results if len(result[1]) >= 4]
    return ocr_text


def connect_to_google_sheets(sheet_name):
    required_vars = [
        "GCP_PROJECT_ID", "GCP_PRIVATE_KEY_ID", "GCP_PRIVATE_KEY",
        "GCP_CLIENT_EMAIL", "GCP_CLIENT_ID", "GCP_CLIENT_X509_CERT_URL"
    ]
    
    for var in required_vars:
        if os.getenv(var) is None:
            raise ValueError(f"Environment variable {var} is not set.")
    
    creds_json = {
        "type": "service_account",
        "project_id": project_id,
        "private_key_id": private_key_id,
        "private_key": private_key,
        "client_email": client_email,
        "client_id": client_id,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": client_x509_cert_url
    }
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json)
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1

def save_to_google_sheets(sheet, results, all_match):
    """Save the comparison results to Google Sheets with match status."""
    # Convert UTC time to Japan Standard Time (JST)
    utc_now = datetime.now(pytz.utc)
    jst_now = utc_now.astimezone(pytz.timezone('Asia/Tokyo'))
    timestamp = jst_now.strftime('%Y-%m-%d %H:%M:%S')
    
    # Ensure results are saved only once
    if 'saved' not in st.session_state:
        st.session_state.saved = False

    if not st.session_state.saved:
        # Append results with match status to Google Sheets
        match_status = "匹敵 (Match)" if all_match else "一致しない (No Match)"
        sheet.append_row(results + [match_status, timestamp])
        st.session_state.saved = True



def main():
    st.title("シンワアクティブ SHINWA ACTIVE")

    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'ocr_results' not in st.session_state:
        st.session_state.ocr_results = []
    if 'saved' not in st.session_state:
        st.session_state.saved = False

    sheet = connect_to_google_sheets("ocr_data")

    if st.session_state.step <= 3:
        st.write(f"Step {st.session_state.step}: 「画像をキャプチャしてください」Capture Image {st.session_state.step}")
        img_file = st.camera_input(f"「画像をキャプチャしてください」Capture Image {st.session_state.step}")

        if img_file:
            image = Image.open(img_file)
            image_np = np.array(image)
            upscaled_image = upscale_image(image_np)
            st.image(image, caption=f'キャプチャされた画像 Captured Image {st.session_state.step}', use_column_width=True)

            ocr_text = perform_ocr(upscaled_image)

            if ocr_text:
                st.write(f"画像から抽出された数字 Extracted Numbers from Image {st.session_state.step}:")
                st.write(ocr_text)
                st.session_state.ocr_results.append(ocr_text)
            else:
                st.write(f"画像に数字が検出されませんでした No numbers detected in Image {st.session_state.step}.")
                st.session_state.ocr_results.append([])

            st.session_state.step += 1
            if st.session_state.step <= 3:
                st.rerun()

    if len(st.session_state.ocr_results) == 3:
        st.write("OCR結果の比較 Comparison of OCR results:")

        results = [ocr[0] if ocr else 'N/A' for ocr in st.session_state.ocr_results[:2]]

        if len(st.session_state.ocr_results[2]) >= 2:
            results.append(st.session_state.ocr_results[2][1][-7:])
        else:
            results.append('N/A')

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

        if not st.session_state.saved:
            # Save results with match status
            save_to_google_sheets(sheet, results, all_match)
            st.write(f"OCR結果がGoogle Sheetsに保存されました Results saved to Google Sheets")

        if st.button("最初からやり直してください。Start Over"):
            # Reset session state
            st.session_state.step = 1
            st.session_state.ocr_results = []
            st.session_state.saved = False
            st.rerun()

if __name__ == "__main__":
    main()
