# model_train.py
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import json

# ---- Paths ----
BASE_DIR     = 'archive/Data'
IMG_DIR      = os.path.join(BASE_DIR, 'train_images')
CSV_PATH     = os.path.join(BASE_DIR, 'train.csv')
MAP_PATH     = os.path.join(BASE_DIR, 'label_num_to_disease_map.json')
TARGET_SIZE  = (160, 160)
BATCH_SIZE   = 8
EPOCHS       = 7

# ---- Load DataFrame and Map ----
df = pd.read_csv(CSV_PATH)
with open(MAP_PATH) as f:
    num2disease = json.load(f)
df.columns = [c.strip().lower() for c in df.columns]   # Normalize column names

# Support both "image" or "image_id" as column name
img_col = 'image' if 'image' in df.columns else 'image_id'
if img_col not in df.columns or 'label' not in df.columns:
    raise ValueError(f"Your CSV must contain columns named 'image' or 'image_id' AND 'label'. Got: {df.columns.tolist()}")

df['disease'] = df['label'].astype(str).map(num2disease)
df['filepath'] = df[img_col].apply(lambda x: os.path.join(IMG_DIR, x))

# ---- Split ----
train_df = df.sample(frac=0.8, random_state=42)
val_df = df.drop(train_df.index)

# ---- Generators ----
datagen = ImageDataGenerator(rescale=1./255)
train_gen = datagen.flow_from_dataframe(
    train_df, x_col='filepath', y_col='disease',
    target_size=TARGET_SIZE, batch_size=BATCH_SIZE,
    class_mode='categorical'
)
val_gen = datagen.flow_from_dataframe(
    val_df, x_col='filepath', y_col='disease',
    target_size=TARGET_SIZE, batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# ---- Model ----
# Use correct method to get number of classes
num_classes = len(train_gen.class_indices)
base = MobileNetV2(weights='imagenet', include_top=False, input_shape=(*TARGET_SIZE, 3))
base.trainable = False
x = GlobalAveragePooling2D()(base.output)
x = Dense(64, activation='relu')(x)
out = Dense(num_classes, activation='softmax')(x)
model = Model(base.input, out)
model.compile(optimizer=Adam(1e-4), loss='categorical_crossentropy', metrics=['accuracy'])

# ---- Train ----
model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS
)

# ---- Save Model and Class Names ----
classes = list(train_gen.class_indices.keys())
os.makedirs('models', exist_ok=True)
model.save('models/disease_model.h5')
np.save('models/class_names.npy', np.array(classes))
print("✅ Model and class names saved:", classes)
