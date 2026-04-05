import pytesseract
import re
import cv2
import os
import numpy as np
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r"G:\TesseractOCR\tesseract.exe"

POPPLER_PATH = r"G:\poppler-25.12.0\Library\bin"


def preprocess_image(img):
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    return thresh


def extract_from_image(img):
    img = preprocess_image(img)

    text = pytesseract.image_to_string(img, config='--oem 3 --psm 6')
    text = text.replace(',', '.')

    amounts = re.findall(r'\d+\.\d{2}', text)

    return text, amounts

def extract_details(text, amounts):
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    merchant = lines[0] if lines else "Unknown"

    date_match = re.search(r'\d{2}[/-]\d{2}[/-]\d{2,4}', text)
    date = date_match.group() if date_match else "Not found"

    if "₹" in text:
        currency = "INR"
    elif "$" in text:
        currency = "USD"
    elif "CHF" in text:
        currency = "CHF"
    elif "EUR" in text:
        currency = "EUR"
    else:
        currency = "Unknown"

    total_amount = amounts[-1] if amounts else "Not found"

    return merchant, date, currency, total_amount


def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    all_text = ""
    all_amounts = []

    if ext in [".jpg", ".jpeg", ".png"]:
        img = cv2.imread(file_path)

        text, amounts = extract_from_image(img)

        all_text += text
        all_amounts.extend(amounts)

    elif ext == ".pdf":
        pages = convert_from_path(file_path, poppler_path=POPPLER_PATH)

        for page in pages:
            img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

            text, amounts = extract_from_image(img)

            all_text += text + "\n"
            all_amounts.extend(amounts)

    else:
        return {"error": "Unsupported file format"}

    merchant, date, currency, total_amount = extract_details(all_text, all_amounts)

    return {
        "merchant": merchant,
        "date": date,
        "currency": currency,
        "amount": total_amount,
        "raw_text": all_text
    }