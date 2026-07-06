import os
from tensorflow.keras.preprocessing import image

input_path = r"D:\Corn_Detection\dataset_1150\Hawar\Hawar_0118.jpg"

output_folder = r"D:\Corn_Detection\preprocessing_output\Hawar"

os.makedirs(output_folder, exist_ok=True)

img = image.load_img(input_path, target_size=(224,224))

output_path = os.path.join(output_folder, "resize_Hawar_0118.jpg")

img.save(output_path)

print("Berhasil disimpan:", output_path)