from flask import Flask, request, jsonify
import os
from ocr import extract_text

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    purpose = request.form.get("purpose")
    claimed_date = request.form.get("date")

    data = extract_text(filepath)

    if claimed_date and data["date"] != "Not found":
        if claimed_date != data["date"]:
            data["date_flag"] = "Mismatch"
        else:
            data["date_flag"] = "OK"

    data["purpose"] = purpose

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)