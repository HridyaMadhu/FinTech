import pytesseract
import re
import cv2
import os
import numpy as np
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r"G:\TesseractOCR\tesseract.exe"

POPPLER_PATH = r"G:\poppler-25.12.0\Library\bin"

def is_blurry(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    return variance < 100

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

def detect_merchant(lines):
    for line in lines:
        if "account name" in line.lower():
            return line.split(":")[-1].strip()
    ignore_words = [
        "receipt", "invoice", "bill", "cash receipt",
        "address", "addr", "tel", "phone", "gst", "tax", "details", "business", "table",
        "server", "guest", "subtotal", "total", "change","thank you", "have a nice day", "welcome",
        "payment terms", "vat", "invoice no", "purchase id",
        "description", "bank", "account", "iban", "swift","branch", "sort code"
    ]

    for line in lines[:10]:
        line_lower = line.lower()

        if any(word in line_lower for word in ignore_words):
            continue

        if re.search(r'\d{2}/\d{2}/\d{4}', line):
            continue  # skip dates

        if re.search(r'\d', line):
            continue  # skip numbers

        if 3 < len(line) < 40:
            return line.strip()

        

    return "Unknown"

def extract_date(text):
    patterns = [
        r'\d{1,2}[A-Z]{3}\d{4}',          
        r'\d{1,2}\s+[A-Za-z]+\s+\d{4}',   
        r'\d{2}[/-]\d{2}[/-]\d{4}'        
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()

    return "Not found"

def detect_currency(text):
    if re.search(r'₹\s*\d', text):
        return "INR"
    elif re.search(r'\$\s*\d', text):
        return "USD"
    elif "EUR" in text:
        return "EUR"
    elif "CHF" in text:
        return "CHF"
    elif "£" in text:
        return "GBP"
    else:
        return "Unknown"

def extract_total(text, amounts):
    total_match = re.search(r'(total|amount)\s*[:\-]?\s*(\d+\.\d{2})', text, re.IGNORECASE)
    gross_match = re.search(r'(gross|grand total)\s*[:\-]?\s*(\d+\.\d{2})', text, re.IGNORECASE)
    net_match = re.search(r'net total\s*[:\-]?\s*(\d+\.\d{2})', text, re.IGNORECASE)

    if total_match:
        total_amount = total_match.group(2)
    elif amounts:
        total_amount = amounts[-1]
    else:
        total_amount = "Not found"

    if gross_match:
        total_amount = gross_match.group(2)
    elif net_match:
        total_amount = net_match.group(1)
    elif amounts:
        total_amount = amounts[-1]

    return total_amount

def extract_details(text, amounts):
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    merchant = detect_merchant(lines)

    date = extract_date(text)
    currency = detect_currency(text)
    total_amount = extract_total(text, amounts)

    return merchant, date, currency, total_amount
    


def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    all_text = ""
    all_amounts = []

    if ext in [".jpg", ".jpeg", ".png"]:
        img = cv2.imread(file_path)

        if is_blurry(img):
            return {"error": "Blurry or unreadable image detected"}

        text, amounts = extract_from_image(img)
        

        all_text += text
        all_amounts.extend(amounts)

    elif ext == ".pdf":
        pages = convert_from_path(file_path, poppler_path=POPPLER_PATH)

        for page in pages:
            img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

            if is_blurry(img):
                return {"error": "Blurry or unreadable PDF page detected"}

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