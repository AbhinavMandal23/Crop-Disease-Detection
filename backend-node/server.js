const express = require("express");
const multer = require("multer");
const axios = require("axios");
const FormData = require("form-data");
const cors = require("cors");

const app = express();
app.use(cors());

const upload = multer();

app.post("/predict", upload.single("file"), async (req, res) => {
  try {

    const formData = new FormData();
    formData.append("file", req.file.buffer, "image.jpg");

    const response = await axios.post(
      "http://127.0.0.1:5001/predict",
      formData,
      { headers: formData.getHeaders() }
    );

    res.json(response.data);

  } catch (error) {
    console.error(error.message);
    res.status(500).json({
      status: "error",
      message: "Error connecting to ML server"
    });
  }
});

app.listen(5001, () => {
  console.log("🚀 Node server running on http://localhost:5001");
});