from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import joblib
import numpy as np
from PIL import Image
import io

# Load model and class mapping
model = load_model("Image_model/models/disease_model.h5")
class_names = np.load("Image_model/models/class_names.npy", allow_pickle=True)

TARGET_SIZE = (160, 160)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    try:
        img = Image.open(io.BytesIO(file.read())).convert('RGB').resize(TARGET_SIZE)
        arr = np.array(img, dtype=np.float32) / 255.0
        arr = arr[np.newaxis, ...]
        probs = model.predict(arr)
        pred_idx = np.argmax(probs)
        pred_class = class_names[pred_idx]
        return jsonify({
            "predicted_class": str(pred_class),
            "confidence": float(np.max(probs))
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def health():
    return "Model prediction API is running."


model = joblib.load('.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    # Expect JSON with N, P, K, temperature, humidity, ph, rainfall
    data = request.json
    features = [
        data['N'],
        data['P'],
        data['K'],
        data['temperature'],
        data['humidity'],
        data['ph'],
        data['rainfall']
    ]
    pred = model.predict([features])[0]
    return jsonify({ 'recommended_crop': pred })


if __name__ == "__main__":
    app.run(debug=True)


