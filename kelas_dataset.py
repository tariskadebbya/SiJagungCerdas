import os

splits = ["train", "val", "test"]
image_ext = (".jpg", ".jpeg", ".png")

def ringkasan_dataset(base_dir, title):
    print(f"\n📊 {title}")
    print("=" * 50)

    classes = sorted(os.listdir(os.path.join(base_dir, "train")))

    for kelas in classes:
        total = 0
        data = {}

        for split in splits:
            path = os.path.join(base_dir, split, kelas)

            if not os.path.exists(path):
                jumlah = 0
            else:
                jumlah = len([
                    f for f in os.listdir(path)
                    if f.lower().endswith(image_ext)
                ])

            data[split] = jumlah
            total += jumlah

        print(f"Kelas: {kelas}")
        print(f"  Train : {data['train']:4d} ({(data['train']/total*100 if total else 0):.2f}%)")
        print(f"  Val   : {data['val']:4d} ({(data['val']/total*100 if total else 0):.2f}%)")
        print(f"  Test  : {data['test']:4d} ({(data['test']/total*100 if total else 0):.2f}%)")
        print(f"  Total : {total}\n")


# ===============================
# PANGGIL UNTUK KEDUA DATASET
# ===============================

ringkasan_dataset("dataset_model1", "DATASET MODEL 1 (JAGUNG vs NON_JAGUNG)")
ringkasan_dataset("dataset_model2", "DATASET MODEL 2 (KLASIFIKASI PENYAKIT)")