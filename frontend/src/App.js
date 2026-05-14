import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const cleanLabel = (text) => {
    return text
      ?.replace(/___/g, " ")
      .replace(/_/g, " ")
      .trim();
  };

  const handleFileChange = (e) => {
    const selected = e.target.files[0];

    if (!selected) return;

    if (!selected.type.startsWith("image/")) {
      alert("Please upload an image.");
      return;
    }

    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setResult(null);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Upload image first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const res = await axios.post(
        "http://localhost:5001/predict",
        formData
      );

      setResult(res.data);

    } catch (err) {
      alert("Server connection failed");
    }

    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>

        <h1 style={styles.title}>
          🌿 Crop Disease Detection
        </h1>

        <p style={styles.subtitle}>
          AI-powered leaf health analysis
        </p>


        <input
          type="file"
          accept="image/*"
          capture="environment"
          onChange={handleFileChange}
          style={styles.input}
        />

        {preview && (
          <img
            src={preview}
            alt="preview"
            style={styles.image}
          />
        )}

        <button
          onClick={handleUpload}
          style={styles.button}
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Predict"}
        </button>


        {result && (
          <div style={styles.resultBox}>

            {result.status === "success" && (
              <>
                <h2 style={styles.disease}>
                  {cleanLabel(result.disease)}
                </h2>

                <div style={styles.bar}>
                  <div
                    style={{
                      ...styles.fill,
                      width: `${result.confidence * 100}%`
                    }}
                  />
                </div>

                <p style={styles.confidence}>
                  Confidence:{" "}
                  {(result.confidence * 100).toFixed(2)}%
                </p>

                {result.latency_ms && (
                  <p style={styles.latency}>
                    ⚡ {result.latency_ms.toFixed(0)} ms
                  </p>
                )}
              </>
            )}

            {result.status === "uncertain" && (
              <p style={styles.warning}>
                ⚠ {result.message}
              </p>
            )}

            {result.status === "invalid" && (
              <p style={styles.error}>
                ❌ {result.message}
              </p>
            )}

          </div>
        )}

      </div>
    </div>
  );
}


const styles = {

  container: {
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background:
      "linear-gradient(to right, #d4fc79, #96e6a1)",
    padding: "20px"
  },

  card: {
    background: "white",
    borderRadius: "20px",
    padding: "30px",
    width: "100%",
    maxWidth: "450px",
    boxShadow:
      "0 10px 30px rgba(0,0,0,0.15)",
    textAlign: "center"
  },

  title: {
    marginBottom: "5px",
    color: "#1b5e20"
  },

  subtitle: {
    color: "#666",
    marginBottom: "20px"
  },

  input: {
    marginBottom: "20px"
  },

  image: {
    width: "100%",
    borderRadius: "15px",
    marginBottom: "20px",
    maxHeight: "300px",
    objectFit: "cover"
  },

  button: {
    width: "100%",
    padding: "14px",
    border: "none",
    borderRadius: "12px",
    background: "#2e7d32",
    color: "white",
    fontSize: "16px",
    cursor: "pointer",
    fontWeight: "bold"
  },

  resultBox: {
    marginTop: "25px"
  },

  disease: {
    color: "#1b5e20"
  },

  bar: {
    width: "100%",
    height: "12px",
    background: "#ddd",
    borderRadius: "10px",
    overflow: "hidden",
    marginTop: "15px"
  },

  fill: {
    height: "100%",
    background: "#4caf50"
  },

  confidence: {
    marginTop: "10px",
    fontWeight: "600"
  },

  latency: {
    color: "#666",
    fontSize: "14px"
  },

  warning: {
    color: "#ef6c00",
    fontWeight: "bold"
  },

  error: {
    color: "#d32f2f",
    fontWeight: "bold"
  }
};

export default App;