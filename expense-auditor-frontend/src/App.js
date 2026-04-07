import React, { useState } from "react";
import bgImage from "./assets/background.webp"; // make sure the image exists

function App() {
  const [file, setFile] = useState(null);
  const [date, setDate] = useState("");
  const [purpose, setPurpose] = useState("");
  const [category, setCategory] = useState("Meals");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [hover, setHover] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("date", date);
    formData.append("purpose", purpose);
    formData.append("category", category);

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
      <h1 style={styles.siteHeading}>📄 Policy-First Expense Auditor</h1>

      <div style={styles.card}>
        <h2 style={styles.cardHeading}>Employee Portal</h2>

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

        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          style={styles.input}
        >
          <option value="Meals">Meals</option>
          <option value="Transport">Transport</option>
          <option value="Lodging">Lodging</option>
        </select>

        <button
          onClick={handleUpload}
          style={{
            ...styles.button,
            background: hover ? "#384959" : "#6a89a7",
          }}
          onMouseEnter={() => setHover(true)}
          onMouseLeave={() => setHover(false)}
        >
          {loading ? "Processing..." : "Upload"}
        </button>

        {result && (
          <div style={styles.result}>
            <p>
              <b>Merchant:</b> {result.merchant}
            </p>
            <p>
              <b>Date:</b> {result.date} ({result.date_flag || "N/A"})
            </p>
            <p>
              <b>Amount:</b> {result.amount} {result.currency}
            </p>
            <p>
              <b>Purpose:</b> {result.purpose}
            </p>
            <p>
              <b>Policy Verdict:</b> {result.policy_verdict}
            </p>
            <p>
              <b>Policy Explanation:</b> {result.policy_explanation}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    backgroundImage: `
      linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)),
      url(${bgImage})
    `,
    backgroundSize: "cover",
    backgroundPosition: "center",
    backgroundRepeat: "no-repeat",

    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    paddingTop: "30px",
  },

  siteHeading: {
    color: "#ffffff",
    fontSize: "2.5rem",
    marginBottom: "20px",
    textShadow: "1px 1px 6px rgba(0,0,0,0.6)",
  },

  card: {
    maxWidth: "500px",
    width: "100%",
    padding: "25px",
    textAlign: "center",
    fontFamily: "Arial",
    background: "rgba(255, 255, 255, 0.9)", // glass effect
    borderRadius: "12px",
    boxShadow: "0 4px 15px rgba(0,0,0,0.2)",
  },

  cardHeading: {
    color: "#384959",
    marginBottom: "20px",
  },

  input: {
    width: "100%",
    margin: "10px 0",
    padding: "10px",
    borderRadius: "6px",
    border: "1px solid #6a89a7",
    outline: "none",
  },

  textarea: {
    width: "100%",
    height: "80px",
    margin: "10px 0",
    padding: "10px",
    borderRadius: "6px",
    border: "1px solid #6a89a7",
    outline: "none",
  },

  button: {
    padding: "12px 25px",
    background: "#6a89a7",
    color: "white",
    border: "none",
    cursor: "pointer",
    borderRadius: "6px",
    fontWeight: "bold",
    transition: "0.3s",
  },

  result: {
    marginTop: "20px",
    padding: "15px",
    background: "#88bdf2",
    borderRadius: "8px",
    textAlign: "left",
    color: "#384959",
  },
};

export default App;