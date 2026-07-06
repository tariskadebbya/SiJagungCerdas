import cv2
import numpy as np
import os

# =========================
# PATH INPUT
# =========================
img_path = r"D:\Corn_Detection\dataset_1150\Hawar\Hawar_0118.jpg"

# =========================
# PATH OUTPUT
# =========================
OUTPUT_DIR = r"D:\Corn_Detection\Segmentasi\Hawar"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# BACA GAMBAR
# =========================
img = cv2.imread(img_path)

if img is None:
    print("Gambar tidak ditemukan!")
    exit()

img_rgb = cv2.cvtColor(
    img,
    cv2.COLOR_BGR2RGB
)

# =========================
# KONVERSI HSV
# =========================
hsv = cv2.cvtColor(
    img,
    cv2.COLOR_BGR2HSV
)

# =========================
# RENTANG WARNA DAUN
# =========================
lower_green = np.array([15, 20, 20])
upper_green = np.array([110, 255, 255])

mask = cv2.inRange(
    hsv,
    lower_green,
    upper_green
)

# =========================
# MORPHOLOGY
# =========================
kernel = np.ones((7,7), np.uint8)

mask = cv2.morphologyEx(
    mask,
    cv2.MORPH_CLOSE,
    kernel,
    iterations=2
)

mask = cv2.dilate(
    mask,
    kernel,
    iterations=2
)

# =========================
# CARI KONTUR TERBESAR
# =========================
contours, _ = cv2.findContours(
    mask,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

if len(contours) == 0:
    print("Kontur daun tidak ditemukan")
    exit()

largest = max(
    contours,
    key=cv2.contourArea
)

# =========================
# BOUNDING BOX
# =========================
x, y, w, h = cv2.boundingRect(
    largest
)

# Tambah margin
padding = 20

x = max(0, x - padding)
y = max(0, y - padding)

w = min(
    img.shape[1] - x,
    w + (padding * 2)
)

h = min(
    img.shape[0] - y,
    h + (padding * 2)
)

# =========================
# CROP DAUN
# =========================
crop_leaf = img_rgb[
    y:y+h,
    x:x+w
]

# =========================
# BACKGROUND REMOVAL
# =========================
background_removed = cv2.bitwise_and(
    img_rgb,
    img_rgb,
    mask=mask
)

# =========================
# BOUNDING BOX IMAGE
# =========================
bbox_img = img_rgb.copy()

cv2.rectangle(
    bbox_img,
    (x, y),
    (x+w, y+h),
    (255, 0, 0),
    3
)

# =========================
# MASK BERWARNA
# =========================
mask_color = cv2.cvtColor(
    mask,
    cv2.COLOR_GRAY2BGR
)

# =========================
# SIMPAN OUTPUT
# =========================
cv2.imwrite(
    os.path.join(
        OUTPUT_DIR,
        "0_original.jpg"
    ),
    img
)

cv2.imwrite(
    os.path.join(
        OUTPUT_DIR,
        "1_mask.jpg"
    ),
    mask_color
)

cv2.imwrite(
    os.path.join(
        OUTPUT_DIR,
        "2_bounding_box.jpg"
    ),
    cv2.cvtColor(
        bbox_img,
        cv2.COLOR_RGB2BGR
    )
)

cv2.imwrite(
    os.path.join(
        OUTPUT_DIR,
        "3_crop_leaf.jpg"
    ),
    cv2.cvtColor(
        crop_leaf,
        cv2.COLOR_RGB2BGR
    )
)

cv2.imwrite(
    os.path.join(
        OUTPUT_DIR,
        "4_background_removed.jpg"
    ),
    cv2.cvtColor(
        background_removed,
        cv2.COLOR_RGB2BGR
    )
)

print("================================")
print("Segmentasi berhasil")
print("Output tersimpan di:")
print(OUTPUT_DIR)
print("================================")