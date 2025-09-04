# test_disease_model.py
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image
import json

print("🔍 Checking environment and files...")

# --- Configuration ---
BASE_DIR = 'archive/Data'
IMG_DIR = os.path.join(BASE_DIR, 'train_images')
CSV_PATH = os.path.join(BASE_DIR, 'train.csv')
MAP_PATH = os.path.join(BASE_DIR, 'label_num_to_disease_map.json')
MODEL_PATH = 'models/disease_model.h5'
CLASSES_PATH = 'models/class_names.npy'
TARGET_SIZE = (160, 160)

# --- File Checks ---
for path in (IMG_DIR, CSV_PATH, MAP_PATH, MODEL_PATH, CLASSES_PATH):
    if not os.path.exists(path):
        print(f"❌ Required file or folder missing: {path}")
        sys.exit(1)
print("✅ All necessary files are available.\n")

# --- Load Label Mapping and Classes ---
try:
    with open(MAP_PATH, encoding='utf-8') as f:
        num2disease = json.load(f)
    class_names = np.load(CLASSES_PATH, allow_pickle=True)
    class_names = class_names.tolist() if isinstance(class_names, np.ndarray) else list(class_names)
    if not class_names:
        raise ValueError('class_names.npy file is empty!')
    print(f"✅ Loaded class mapping ({len(class_names)} classes): {class_names}")
except Exception as e:
    print(f"❌ Error loading classes or mapping: {e}")
    sys.exit(1)

# --- Load CSV and Set Up DataFrame ---
try:
    df = pd.read_csv(CSV_PATH)
except Exception as e:
    print(f"❌ Failed to open CSV: {e}")
    sys.exit(1)

df.columns = [c.strip().lower() for c in df.columns]
if 'image_id' in df.columns:
    img_col = 'image_id'
elif 'image' in df.columns:
    img_col = 'image'
else:
    print("❌ CSV missing required 'image' or 'image_id' column")
    sys.exit(1)
if 'label' not in df.columns:
    print("❌ CSV missing required 'label' column")
    sys.exit(1)

df['disease'] = df['label'].astype(str).map(num2disease)
df['filepath'] = df[img_col].apply(lambda x: os.path.normpath(os.path.join(IMG_DIR, x)))

# --- Filter for missing files up front & Optionally use ≤ 200 for speed ---
missing = ~df['filepath'].apply(os.path.exists)
num_missing = missing.sum()
if num_missing > 0:
    print(f"⚠️ Warning: {num_missing} of {len(df)} listed images are missing and will be skipped.")
df = df[~missing]
if len(df) > 200:
    df = df.sample(n=200, random_state=42).reset_index(drop=True)
print(f"Testing on {len(df)} existing images, {len(class_names)} classes.")

# --- Load Model ---
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Model loaded.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    sys.exit(1)

# --- Prediction Loop ---
y_true, y_pred = [], []
print("🔬 Running predictions...")
for idx, row in df.iterrows():
    img_path = row['filepath']
    label = row['disease']
    try:
        img = Image.open(img_path).convert('RGB').resize(TARGET_SIZE)
        arr = np.array(img, dtype=np.float32) / 255.0
        arr = arr[np.newaxis, ...]
        pred_probs = model.predict(arr, verbose=0)
        pred_idx = np.argmax(pred_probs)
        pred_label = class_names[pred_idx]
    except Exception as e:
        print(f"⚠️ Error with image {img_path}: {e}")
        continue
    y_true.append(label)
    y_pred.append(pred_label)
    if (idx + 1) % 50 == 0 or (idx + 1) == len(df):
        print(f"  Predicted {idx + 1}/{len(df)} images")

print(f"\n✅ Predictions completed for {len(y_true)} samples (skipped {num_missing} missing files)")

# --- Metrics Report ---
try:
    from sklearn.metrics import classification_report, confusion_matrix
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, zero_division=0))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_true, y_pred))
except Exception as e:
    print(f"❌ Error computing metrics: {e}")

print("\n🎉 Model testing and reporting complete.")
