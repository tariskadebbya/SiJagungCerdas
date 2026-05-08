# predict.py

import os
import numpy as np
import tensorflow as tf

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# KERAS 3 - LOAD SAVEDMODEL
from keras.layers import TFSMLayer

# ===============================
# SUPPRESS WARNING TF
# ===============================
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# ===============================
# BASE PATH
# ===============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ===============================
# PATH MODEL
# ===============================
MODEL1_PATH = os.path.join(BASE_DIR, "model_model1", "saved_model1")
MODEL2_PATH = os.path.join(BASE_DIR, "model_model2", "saved_model2")

# ===============================
# LOAD MODEL
# ===============================
print("Loading Model 1...")
model1 = TFSMLayer(MODEL1_PATH, call_endpoint="serve")

print("Loading Model 2...")
model2 = TFSMLayer(MODEL2_PATH, call_endpoint="serve")

print("Model berhasil dimuat ✔")

# ===============================
# LABEL
# ===============================
LABELS_MODEL1 = ["jagung", "non_jagung"]

LABELS_MODEL2 = [
    "hawar_daun",
    "karat_daun",
    "sehat"
]

# ===============================
# PREPROCESS IMAGE
# ===============================
def preprocess_image(img_path, size):

    img = image.load_img(
        img_path,
        target_size=size
    )

    img_array = image.img_to_array(img)

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    img_array = preprocess_input(img_array)

    return img_array

# ===============================
# PREDICT IMAGE
# ===============================
def predict_image(image_path):

    # ===========================
    # CHECK FILE
    # ===========================
    if not os.path.exists(image_path):
        raise FileNotFoundError(
            "File gambar tidak ditemukan"
        )

    print("\n==============================")
    print("PREDIKSI GAMBAR")
    print("==============================")

    # ===========================
    # MODEL 1
    # JAGUNG / NON JAGUNG
    # ===========================
    img1 = preprocess_image(
        image_path,
        (128, 128)
    )

    preds1 = model1(img1)
    preds1 = preds1.numpy()[0]

    idx1 = np.argmax(preds1)

    label1 = LABELS_MODEL1[idx1]

    conf1 = float(preds1[idx1]) * 100

    print("\n--- MODEL 1 ---")
    print("Prediksi :", label1)
    print("Confidence :", f"{conf1:.2f}%")

    # ===========================
    # JIKA NON JAGUNG
    # ===========================
    if label1 == "non_jagung":

        return {
            "status": "non_jagung",
            "penyakit": None,
            "confidence": round(conf1, 2)
        }

    # ===========================
    # MODEL 2
    # PENYAKIT JAGUNG
    # ===========================
    img2 = preprocess_image(
        image_path,
        (224, 224)
    )

    preds2 = model2(img2)
    preds2 = preds2.numpy()[0]

    idx2 = np.argmax(preds2)

    label2 = LABELS_MODEL2[idx2]

    conf2 = float(preds2[idx2]) * 100

    print("\n--- MODEL 2 ---")
    print("Prediksi :", label2)
    print("Confidence :", f"{conf2:.2f}%")

    return {
        "status": "jagung",
        "penyakit": label2,
        "confidence": round(conf2, 2)
    }

# ===============================
# TEST MANUAL
# ===============================
if __name__ == "__main__":

    IMAGE_PATH = os.path.join(
        BASE_DIR,
        "test_image5.jpg"
    )

    result = predict_image(IMAGE_PATH)

    print("\n==============================")
    print("HASIL AKHIR")
    print("==============================")

    print(result)