import os
import shutil
import random

SOURCE_DIR = "../dataset"
TARGET_DIR = "dataset_model1"

TRAIN_RATIO = 0.8
VAL_RATIO   = 0.10
TEST_RATIO  = 0.10

random.seed(42)

JAGUNG_CLASSES = ["hawar_daun", "karat_daun", "sehat"]

for split in ["train", "val", "test"]:
    os.makedirs(os.path.join(TARGET_DIR, split, "jagung"), exist_ok=True)
    os.makedirs(os.path.join(TARGET_DIR, split, "non_jagung"), exist_ok=True)

for class_name in os.listdir(SOURCE_DIR):
    class_path = os.path.join(SOURCE_DIR, class_name)

    if not os.path.isdir(class_path):
        continue

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

    # 🔥 Tentukan label
    if class_name in JAGUNG_CLASSES:
        label = "jagung"
    else:
        label = "non_jagung"

    for split_name, split_images in splits.items():
        target_dir = os.path.join(TARGET_DIR, split_name, label)

        for img in split_images:
            src = os.path.join(class_path, img)
            dst = os.path.join(target_dir, f"{class_name}_{img}")
            shutil.copy2(src, dst)

    print(f"✅ {class_name} → {label}")

print("🎉 Model 1 dataset siap!")