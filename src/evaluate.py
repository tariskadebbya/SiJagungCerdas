# evaluate_model.py
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# ===============================
# PATH MODEL & DATA
# ===============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.h5")
TEST_DIR = os.path.join(BASE_DIR, "dataset_split", "test")

# ===============================
# EVALUASI MODEL
# ===============================
def evaluate_model(img_size=(224,224), batch_size=16):

    print("Load model:", MODEL_PATH)
    model = load_model(MODEL_PATH, compile=False)

    datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

    test_gen = datagen.flow_from_directory(
        TEST_DIR,
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical",
        shuffle=False
    )

    class_names = list(test_gen.class_indices.keys())
    print("\nClass Names:", class_names)

    print("\nPredicting test data...")
    preds = model.predict(test_gen, verbose=1)

    y_pred = np.argmax(preds, axis=1)
    y_true = test_gen.classes

    # ===============================
    # CONFUSION MATRIX (SEMUA KELAS)
    # ===============================
    cm = confusion_matrix(
        y_true,
        y_pred,
        labels=list(range(len(class_names)))
    )

    print("\n=== CONFUSION MATRIX (SEMUA KELAS) ===")
    print(cm)

    # ===============================
    # CLASSIFICATION REPORT
    # ===============================
    print("\n=== CLASSIFICATION REPORT ===")
    print(classification_report(
        y_true,
        y_pred,
        labels=list(range(len(class_names))),
        target_names=class_names,
        digits=4
    ))

    # ===============================
    # VISUALISASI CONFUSION MATRIX
    # ===============================
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=class_names
    )

    disp.plot(cmap=plt.cm.Blues, values_format="d")
    plt.title("Confusion Matrix (Semua Kelas)")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    evaluate_model()