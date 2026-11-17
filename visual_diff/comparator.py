import cv2
import numpy as np


def find_differences(baseline, current, threshold=10):
    """
    Compare two images and find regions with differences above threshold.

    Returns list of difference regions as dicts with 'x', 'y', 'w', 'h' keys.
    Threshold is based on pixel count (number of changed pixels).
    Uses connected components to accurately count pixels per region.
    """
    diff = cv2.absdiff(baseline, current)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(gray_diff, 1, 255, cv2.THRESH_BINARY)

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)

    differences = []
    for label_idx in range(1, num_labels):
        pixel_count = stats[label_idx, cv2.CC_STAT_AREA]

        if pixel_count >= threshold:
            x = stats[label_idx, cv2.CC_STAT_LEFT]
            y = stats[label_idx, cv2.CC_STAT_TOP]
            w = stats[label_idx, cv2.CC_STAT_WIDTH]
            h = stats[label_idx, cv2.CC_STAT_HEIGHT]
            differences.append({"x": x, "y": y, "w": w, "h": h})

    return differences
