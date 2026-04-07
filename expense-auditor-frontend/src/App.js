import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [date, setDate] = useState("");
  const [purpose, setPurpose] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("date", date);
    formData.append("purpose", purpose);

    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Error uploading file");
    }

    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <h2>📄 Policy-First Expense Auditor</h2>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        style={styles.input}
      />

      <input
        type="date"
        value={date}
        onChange={(e) => setDate(e.target.value)}
        style={styles.input}
      />

      <textarea
        placeholder="Enter Business Purpose"
        value={purpose}
        onChange={(e) => setPurpose(e.target.value)}
        style={styles.textarea}
      />

      <button onClick={handleUpload} style={styles.button}>
        {loading ? "Processing..." : "Upload"}
      </button>

      {result && (
        <div style={styles.result}>
          <p><b>Merchant:</b> {result.merchant}</p>
          <p><b>Date:</b> {result.date} ({result.date_flag || "N/A"})</p>
          <p><b>Amount:</b> {result.amount} {result.currency}</p>
          <p><b>Purpose:</b> {result.purpose}</p>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "500px",
    margin: "50px auto",
    padding: "20px",
    textAlign: "center",
    fontFamily: "Arial",
    background: "#f9f9f9",
    borderRadius: "10px",
    boxShadow: "0 0 10px rgba(0,0,0,0.1)"
  },
  input: {
    width: "100%",
    margin: "10px 0",
    padding: "10px"
  },
  textarea: {
    width: "100%",
    height: "80px",
    margin: "10px 0",
    padding: "10px"
  },
  button: {
    padding: "10px 20px",
    background: "#007bff",
    color: "white",
    border: "none",
    cursor: "pointer",
    borderRadius: "5px"
  },
  result: {
    marginTop: "20px",
    padding: "15px",
    background: "#e6f0ff",
    borderRadius: "8px",
    textAlign: "left"
  }
};

export default App;