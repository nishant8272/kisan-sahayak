import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import sys
import os

def train_crop_model(data_path="crop_detection.csv", model_path="crop_model.pkl", encoder_path="label_encoder.pkl"):
    try:
        # ---------------- Step 1: Load dataset ----------------
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"❌ Dataset not found: {data_path}")

        df = pd.read_csv(data_path)

        required_cols = ["N", "P", "K", "ph", "temperature", "humidity", "rainfall", "label"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"❌ Missing required column: {col}")

        print(f"✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

        # ---------------- Step 2: Features & Labels ----------------
        X = df[["N", "P", "K", "ph", "temperature", "humidity", "rainfall"]]
        y = df["label"]

        if X.isnull().any().any() or y.isnull().any():
            raise ValueError("❌ Dataset contains missing values. Please clean your data.")

        # ---------------- Step 3: Encode Labels ----------------
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        print(f"✅ Crops encoded: {len(le.classes_)} unique crops")

        # ---------------- Step 4: Train/Test Split ----------------
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )

        print(f"✅ Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")

        # ---------------- Step 5: Train Model ----------------
        model = RandomForestClassifier(
            n_estimators=300,
            random_state=42,
            max_depth=20,
            class_weight="balanced"
        )

        model.fit(X_train, y_train)
        print("✅ Model training completed")

        # ---------------- Step 6: Evaluate ----------------
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"📊 Accuracy: {acc:.2%}")
        print("\nClassification Report:\n")
        print(classification_report(y_test, y_pred, target_names=le.classes_))

        # ---------------- Step 7: Save Model ----------------
        joblib.dump(model, model_path)
        joblib.dump(le, encoder_path)

        print(f"✅ Model saved at: {model_path}")
        print(f"✅ Label Encoder saved at: {encoder_path}")

        return model, le

    except FileNotFoundError as fnf:
        print(fnf)
        sys.exit(1)

    except ValueError as ve:
        print(ve)
        sys.exit(1)

    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)


# ---------------- Run Training ----------------
if __name__ == "__main__":
    train_crop_model()
