from tensorflow.keras.models import load_model

print("Loading Model 1...")
model1 = load_model("../model_model1/model1_FINAL.keras", compile=False)

print("Loading Model 2...")
model2 = load_model("../model_model2/model2_FINAL.keras", compile=False)

print("SEMUA MODEL BERHASIL DIMUAT")