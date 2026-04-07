from flask import Flask, request, jsonify
import os
from ocr import extract_text
from flask_cors import CORS
import PyPDF2
import re
from datetime import datetime
from dateutil import parser

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
POLICY_PATH = "GTP-Travel-and-Expense-Policy.pdf"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def load_policy(path):
    if not os.path.exists(path):
        return ""
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

POLICY_TEXT = load_policy(POLICY_PATH)

def check_policy(amount, category, text=None):
    limits = {
        "Meals": 50,
        "Transport": 100,
        "Lodging": 200
    }

    pattern = re.compile(rf"{category}.*?limit.*?(\d+)", re.IGNORECASE | re.DOTALL)
    match = pattern.search(POLICY_TEXT)
    if match:
        limits[category] = float(match.group(1))

    prohibited_items = ["alcohol", "liquor", "cigarettes"]
    flagged = []
    if text:
        for item in prohibited_items:
            if re.search(rf"\b{item}\b", text, re.IGNORECASE):
                flagged.append(item)

    if amount == "Not found":
        return {"verdict": "Flagged", "explanation": "Amount not detected in receipt"}

    try:
        amt = float(amount)
    except:
        return {"verdict": "Flagged", "explanation": "Invalid amount format"}

    if amt > limits.get(category, float("inf")):
        return {
            "verdict": "Rejected",
            "explanation": f"Amount {amt} exceeds {category} limit of {limits[category]} as per policy"
        }
    elif flagged:
        return {
            "verdict": "Flagged",
            "explanation": f"Receipt contains prohibited item(s): {', '.join(flagged)}"
        }
    else:
        return {
            "verdict": "Approved",
            "explanation": f"Receipt amount {amt} is within {category} limit of {limits[category]}"
        }

def normalize_date(date_str):
    try:
        return parser.parse(date_str).strftime("%Y-%m-%d")
    except:
        return None
    
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    purpose = request.form.get("purpose")
    claimed_date = request.form.get("date")
    category = request.form.get("category", "Meals")

    data = extract_text(filepath)

    if "error" in data:
        return jsonify(data), 400

    if claimed_date and data["date"] != "Not found":
        normalized_claimed = normalize_date(claimed_date)
        normalized_detected = normalize_date(data["date"])

        if normalized_claimed and normalized_detected:
            if normalized_claimed != normalized_detected:
                data["date_flag"] = "Mismatch"
            else:
                data["date_flag"] = "OK"
        else:
            data["date_flag"] = "Could not normalize date"

    verdict_info = check_policy(data["amount"], category, text=data["raw_text"])
    data["policy_verdict"] = verdict_info["verdict"]
    data["policy_explanation"] = verdict_info["explanation"]
    data["purpose"] = purpose

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)