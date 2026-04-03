import pytesseract
from PIL import Image
import re
import cv2
import re
import os
import numpy as np
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r"G:\TesseractOCR\tesseract.exe"

def preprocess(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)


    return thresh
   

def extract_text(image_path):
    img = preprocess(image_path)

    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=custom_config)

    # Normalize commas to dots
    text = text.replace(',', '.')

    # Extract all decimal numbers
    amounts = re.findall(r'\d+\.\d{2}', text)

    return {
        "raw_text": text,
        "amount": amounts[-1] if amounts else "Not found"
    }

