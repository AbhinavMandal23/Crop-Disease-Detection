from flask import Flask, request, jsonify
from flask_cors import CORS 
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import time

app = Flask(__name__)
CORS(app)

# -------------------------
# PATHS
# -------------------------
MODEL_PATH = r"C:\Users\KIIT0001\Projects\Mini-Project\Crop-Disease_Detection_Using-CNN\model\crop_model.h5"
CLASS_NAMES_PATH = r"C:\Users\KIIT0001\Projects\Mini-Project\Crop-Disease_Detection_Using-CNN\model\class_names.json"

# -------------------------
# LOAD MODEL
# -------------------------
model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_NAMES_PATH) as f:
    class_names = json.load(f)

# -------------------------
# PREPROCESS
# -------------------------
def preprocess(img):
    img = img.resize((224, 224))
    img = np.array(img)

    # basic sanity check (very dark / bright images)
    if np.mean(img) < 20 or np.mean(img) > 240:
        return None

    img = img / 255.0
    return np.expand_dims(img, axis=0)

# -------------------------
# ROUTE
# -------------------------
@app.route("/predict", methods=["POST"])
def predict():
    start = time.perf_counter()
    try:
        file = request.files["file"]
        img = Image.open(file).convert("RGB")

        processed = preprocess(img)

        if processed is None:
            return jsonify({
                "status": "invalid",
                "message": "Invalid image. Please upload a clear leaf image."
            })

        pred = model.predict(processed)
        class_index = int(np.argmax(pred))
        confidence = float(np.max(pred))
        disease_name = class_names[class_index]

        # confidence threshold
        if confidence < 0.7:
            return jsonify({
                "status": "uncertain",
                "disease": "Uncertain result",
                "confidence": confidence,
                "message": "Please upload a clearer leaf image"
            })

        # healthy handling
        if "healthy" in disease_name.lower():
            disease_name = "Healthy Leaf"
            
        end=time.perf_counter()
        latency=(end - start )*1000
        print(f"API Latency: {latency:.2f} ms")
        return jsonify({
            "status": "success",
            "disease": disease_name,
            "confidence": confidence
        })

    except Exception as e:
        
        return jsonify({
            "status": "error",
            "message": str(e)
        })

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5001)