import cv2
import numpy as np


def find_differences(baseline, current, threshold=10):
    """
    Compare two images and find regions with differences above threshold.

    Returns list of difference regions as dicts with 'x', 'y', 'w', 'h' keys.
    Differences with area < threshold are filtered out.
    """
    diff = cv2.absdiff(baseline, current)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(gray_diff, 1, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    differences = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area >= threshold:
            x, y, w, h = cv2.boundingRect(contour)
            differences.append({"x": x, "y": y, "w": w, "h": h})

    return differences
