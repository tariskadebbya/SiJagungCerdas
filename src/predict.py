# predict.py

import os
import pickle
import numpy as np
import tensorflow as tf

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from keras.layers import TFSMLayer

# ===============================
# SUPPRESS WARNING TF
# ===============================
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# ===============================
# BASE DIR
# ===============================
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# ===============================
# PATH MODEL
# ===============================
MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "saved_model"
)

CLASS_PATH = os.path.join(
    BASE_DIR,
    "model",
    "class_names1.pkl"
)

# ===============================
# LOAD MODEL
# ===============================
print("Loading Model...")

model = TFSMLayer(
    MODEL_PATH,
    call_endpoint="serve"
)

print("✅ Model berhasil dimuat")

# ===============================
# LOAD CLASS NAMES
# ===============================
with open(CLASS_PATH, "rb") as f:
    CLASS_NAMES = pickle.load(f)

print("Class Names:")
print(CLASS_NAMES)

# ===============================
# PREPROCESS IMAGE
# ===============================
def preprocess_image(img_path):

    img = image.load_img(
        img_path,
        target_size=(224, 224)
    )

    img_array = image.img_to_array(img)

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    img_array = preprocess_input(
        img_array
    )

    return img_array

# ===============================
# PREDICT IMAGE
# ===============================
def predict_image(image_path):

    if not os.path.exists(image_path):

        raise FileNotFoundError(
            "File gambar tidak ditemukan"
        )

    img = preprocess_image(
        image_path
    )

    preds = model(img)

    preds = preds.numpy()[0]

    idx = np.argmax(preds)

    label = CLASS_NAMES[idx]

    confidence = float(
        preds[idx]
    ) * 100

    return {
        "kelas": label,
        "confidence": round(
            confidence,
            2
        ),
        "probabilities": {
            CLASS_NAMES[i]:
            round(
                float(preds[i]) * 100,
                2
            )
            for i in range(len(CLASS_NAMES))
        }
    }

# ===============================
# TEST MANUAL
# ===============================
if __name__ == "__main__":

    IMAGE_PATH = os.path.join(
        BASE_DIR,
        "test_image4.jpg"
    )

    result = predict_image(
        IMAGE_PATH
    )

    print("\n====================")
    print("HASIL PREDIKSI")
    print("====================")

    print(
        f"Kelas      : {result['kelas']}"
    )

    print(
        f"Confidence : {result['confidence']}%"
    )

    print("\nProbabilitas:")

    for k, v in result["probabilities"].items():

        print(
            f"{k:<15}: {v:.2f}%"
        )