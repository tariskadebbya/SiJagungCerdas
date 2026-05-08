import os
import random
import matplotlib.pyplot as plt

# ===============================
# PATH DATASET
# ===============================
image_dir = "../dataset"  # sesuaikan

# jumlah gambar per kelas
num_samples = 5

# ambil kelas
class_folders = sorted([
    f for f in os.listdir(image_dir)
    if os.path.isdir(os.path.join(image_dir, f))
])

# ===============================
# BUAT GRID
# ===============================
rows = len(class_folders)
cols = num_samples

fig, axes = plt.subplots(rows, cols, figsize=(cols*3, rows*3))

# kalau cuma 1 kelas biar tidak error
if rows == 1:
    axes = [axes]

for row, class_name in enumerate(class_folders):
    class_path = os.path.join(image_dir, class_name)

    images = [
        f for f in os.listdir(class_path)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ]

    if len(images) == 0:
        continue

    # ambil random
    images = random.sample(images, min(num_samples, len(images)))

    for col in range(cols):
        ax = axes[row][col] if rows > 1 else axes[col]

        if col < len(images):
            img_path = os.path.join(class_path, images[col])
            img = plt.imread(img_path)
            ax.imshow(img)
        else:
            ax.imshow([[0]])  # kosong kalau kurang

        ax.axis("off")

        # kasih label di kolom pertama
        if col == 0:
            ax.set_title(class_name, loc='left', fontsize=10)

plt.tight_layout()
plt.show()