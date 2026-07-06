import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image

# =========================
# PATH GAMBAR ASLI
# =========================
img_path = r"D:\Corn_Detection\dataset_1150\Hawar\Hawar_0118.jpg"

# =========================
# FOLDER OUTPUT
# =========================
output_dir = r"D:\Corn_Detection\augmentation"
os.makedirs(output_dir, exist_ok=True)

# =========================
# LOAD IMAGE
# =========================
img = image.load_img(img_path, target_size=(224,224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)

# Simpan gambar asli
img.save(os.path.join(output_dir, "asli.jpg"))

# =========================
# FUNGSI SIMPAN AUGMENTASI
# =========================
def save_augmented_image(datagen, filename):
    aug_iter = datagen.flow(img_array, batch_size=1)

    batch = next(aug_iter)

    img_aug = batch[0].astype("uint8")

    Image.fromarray(img_aug).save(
        os.path.join(output_dir, filename)
    )

# =========================
# ROTATION
# =========================
rotation_gen = ImageDataGenerator(
    rotation_range=20
)

save_augmented_image(rotation_gen, "rotasi.jpg")

# =========================
# ZOOM
# =========================
zoom_gen = ImageDataGenerator(
    zoom_range=0.2
)

save_augmented_image(zoom_gen, "zoom.jpg")

# =========================
# HORIZONTAL FLIP
# =========================
flip_gen = ImageDataGenerator(
    horizontal_flip=True
)

save_augmented_image(flip_gen, "horizontal_flip.jpg")

# =========================
# BRIGHTNESS
# =========================
brightness_gen = ImageDataGenerator(
    brightness_range=[0.8,1.2]
)

save_augmented_image(brightness_gen, "brightness.jpg")

# =========================
# WIDTH SHIFT
# =========================
width_shift_gen = ImageDataGenerator(
    width_shift_range=0.1
)

save_augmented_image(width_shift_gen, "width_shift.jpg")

# =========================
# HEIGHT SHIFT
# =========================
height_shift_gen = ImageDataGenerator(
    height_shift_range=0.1
)

save_augmented_image(height_shift_gen, "height_shift.jpg")

# =========================
# SHEAR
# =========================
shear_gen = ImageDataGenerator(
    shear_range=0.1
)

save_augmented_image(shear_gen, "shear.jpg")

print("===================================")
print("Semua hasil augmentasi berhasil disimpan")
print("Lokasi :", output_dir)
print("===================================")