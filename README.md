Policy-First Expense Auditor
The Problem

Organizations often face challenges in manually verifying employee expense claims against company policies. This process is time-consuming, error-prone, and difficult to scale, especially when dealing with large volumes of receipts and complex policy documents.

The Solution

The Policy-First Expense Auditor is an AI-powered system that automates receipt validation by combining OCR (Optical Character Recognition) with intelligent policy analysis.It:

- Extracts key details from receipts (merchant, date, amount, currency)
- Cross-references extracted data with company travel & expense policies
- Detects violations such as:
  - Exceeding category limits (Meals, Transport, Lodging)
  - Presence of prohibited items (e.g., alcohol, cigarettes)
- Provides a clear verdict:
  - Approved
  -Flagged
  - Rejected

Key Features

- OCR-based receipt scanning (images & PDFs)
- Automatic extraction of:
  - Merchant name
  - Date
  - Amount & currency
- Policy-based validation engine
- Smart decision system (Approved / Flagged / Rejected)
- Date mismatch detection
- User-friendly React interface

Tech Stack

Backend
- Python
- Flask
- PyTesseract (OCR)
- OpenCV (Image preprocessing)
- pdf2image
- PyPDF2

Frontend
- React.js
- HTML/CSS (inline styling)

Libraries & Tools
- dateutil (date parsing)
- Flask-CORS




Setup Instructions
1. Clone the Repository
git clone https://github.com/your-username/expense-auditor.git
cd expense-auditor
2. Backend Setup
Install dependencies
pip install flask flask-cors pytesseract opencv-python pdf2image PyPDF2 python-dateutil numpy
Install Required Tools
Install Tesseract OCR
Install Poppler

Update paths in your code:

pytesseract.pytesseract.tesseract_cmd = "YOUR_PATH_TO_TESSERACT"
POPPLER_PATH = "YOUR_PATH_TO_POPPLER"
Run Backend
python app.py

Backend runs on:

http://127.0.0.1:5000
3. Frontend Setup
cd frontend
npm install
npm start

Frontend runs on:

http://localhost:3000

How It Works
- User uploads a receipt (image or PDF)
- OCR extracts raw text from the file
- System detects:
  - Amount
  - Date
  - Merchant
- Policy engine:
  - Reads company policy PDF
  - Applies limits & rules
- Final verdict is generated and shown in UI
