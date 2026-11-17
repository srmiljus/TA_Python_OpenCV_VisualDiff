import os
import cv2


def validate_image_file(path: str, label: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{label} file not found: {path}")

    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"{label} is not a valid image file: {path}")

    return img


def validate_dimensions(img1, img2):
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    if (h1, w1) != (h2, w2):
        raise ValueError(f"Image dimensions mismatch: baseline ({h1}, {w1}) vs current ({h2}, {w2})")
