import os
import shutil
import random

SOURCE_DIR = "../dataset"
TARGET_DIR = "dataset_model2"

TRAIN_RATIO = 0.8
VAL_RATIO   = 0.10
TEST_RATIO  = 0.10

random.seed(42)

VALID_CLASSES = ["hawar_daun", "karat_daun", "sehat"]

for class_name in VALID_CLASSES:
    class_path = os.path.join(SOURCE_DIR, class_name)

    images = [
        img for img in os.listdir(class_path)
        if img.lower().endswith((".jpg", ".png", ".jpeg"))
    ]

    random.shuffle(images)

    total = len(images)
    train_end = int(total * TRAIN_RATIO)
    val_end   = train_end + int(total * VAL_RATIO)

    splits = {
        "train": images[:train_end],
        "val":   images[train_end:val_end],
        "test":  images[val_end:]
    }

    for split_name, split_images in splits.items():
        target_dir = os.path.join(TARGET_DIR, split_name, class_name)
        os.makedirs(target_dir, exist_ok=True)

        for img in split_images:
            src = os.path.join(class_path, img)
            dst = os.path.join(target_dir, img)
            shutil.copy2(src, dst)

    print(f"✅ {class_name} diproses")

print("🎉 Model 2 dataset siap!")