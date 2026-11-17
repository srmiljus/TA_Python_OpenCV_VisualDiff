import pytest
import numpy as np
import cv2
import tempfile
import os


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def temp_images_dir():
    """Create a temporary directory for input test images."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def identical_image():
    """Create a white image with known dimensions."""
    return np.ones((100, 100, 3), dtype=np.uint8) * 255


@pytest.fixture
def baseline_image():
    """Create a baseline image (white background)."""
    return np.ones((100, 100, 3), dtype=np.uint8) * 255


@pytest.fixture
def current_image_with_small_change():
    """Create current image with a small change (< 10 pixels)."""
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    img[10:13, 10:13] = [0, 0, 255]  # 3x3 red square = 9 pixels (below threshold)
    return img


@pytest.fixture
def current_image_with_threshold_change():
    """Create current image with change at threshold (10 pixels)."""
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    img[10:14, 10:12] = [0, 0, 255]  # 4x2 red rectangle = 8 pixels, plus border effects
    return img


@pytest.fixture
def current_image_with_large_change():
    """Create current image with a large change (> 10 pixels)."""
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    img[10:20, 10:20] = [0, 0, 255]  # 10x10 red square
    return img


@pytest.fixture
def current_image_with_two_changes():
    """Create current image with two separate changes."""
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    img[10:20, 10:20] = [0, 0, 255]  # First change: 10x10 square
    img[60:70, 60:70] = [0, 255, 0]  # Second change: 10x10 square
    return img


@pytest.fixture
def current_image_with_20px_change():
    """Create current image with a 20-pixel change."""
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    img[10:15, 10:14] = [0, 0, 255]  # 5x4 red rectangle = 20 pixels
    return img


@pytest.fixture
def current_image_with_thin_line():
    """Create current image with a thin horizontal line change (1x100 pixels)."""
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    img[50, 0:100] = [0, 0, 255]  # Horizontal line 1x100 = 100 pixels
    return img


@pytest.fixture
def current_image_with_5x4_block():
    """Create current image with a 5x4 block change (20 pixels)."""
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    img[10:15, 10:14] = [0, 0, 255]  # 5x4 red rectangle = 20 pixels
    return img


@pytest.fixture
def images_with_overlapping_regions_files(temp_images_dir):
    """Create images with two separate regions: vertical line and U shape."""
    baseline = np.ones((150, 60, 3), dtype=np.uint8) * 255
    current = np.ones((150, 60, 3), dtype=np.uint8) * 255

    current[10:110, 20] = [0, 0, 255]  # Vertical line 100x1 px
    current[5, 16:25] = [0, 0, 255]    # Top of U: 1x9 px
    current[6:15, 16] = [0, 0, 255]    # Left side of U: 9x1 px
    current[6:15, 24] = [0, 0, 255]    # Right side of U: 9x1 px
    # Total U: 9 + 9 + 9 = 27 pixels (doesn't touch line)

    baseline_path = os.path.join(temp_images_dir, "baseline.png")
    current_path = os.path.join(temp_images_dir, "current.png")

    cv2.imwrite(baseline_path, baseline)
    cv2.imwrite(current_path, current)

    return baseline_path, current_path


@pytest.fixture
def temp_image_files(baseline_image, current_image_with_large_change, temp_images_dir):
    """Create temporary image files for CLI tests."""
    baseline_path = os.path.join(temp_images_dir, "baseline.png")
    current_path = os.path.join(temp_images_dir, "current.png")

    cv2.imwrite(baseline_path, baseline_image)
    cv2.imwrite(current_path, current_image_with_large_change)

    return baseline_path, current_path


@pytest.fixture
def identical_images_files(identical_image, temp_images_dir):
    """Create temporary files with identical images."""
    baseline_path = os.path.join(temp_images_dir, "baseline.png")
    current_path = os.path.join(temp_images_dir, "current.png")

    cv2.imwrite(baseline_path, identical_image)
    cv2.imwrite(current_path, identical_image)

    return baseline_path, current_path


@pytest.fixture
def images_with_two_changes_files(baseline_image, current_image_with_two_changes, temp_images_dir):
    """Create temporary files with two separate changes."""
    baseline_path = os.path.join(temp_images_dir, "baseline.png")
    current_path = os.path.join(temp_images_dir, "current.png")

    cv2.imwrite(baseline_path, baseline_image)
    cv2.imwrite(current_path, current_image_with_two_changes)

    return baseline_path, current_path


@pytest.fixture
def images_different_dimensions_files(temp_images_dir):
    """Create temporary files with different dimensions."""
    baseline_path = os.path.join(temp_images_dir, "baseline.png")
    current_path = os.path.join(temp_images_dir, "current.png")

    img1 = np.ones((100, 100, 3), dtype=np.uint8) * 255
    img2 = np.ones((50, 75, 3), dtype=np.uint8) * 255

    cv2.imwrite(baseline_path, img1)
    cv2.imwrite(current_path, img2)

    return baseline_path, current_path


@pytest.fixture
def images_with_20px_change_files(baseline_image, current_image_with_20px_change, temp_images_dir):
    """Create temporary files with 20-pixel change."""
    baseline_path = os.path.join(temp_images_dir, "baseline.png")
    current_path = os.path.join(temp_images_dir, "current.png")

    cv2.imwrite(baseline_path, baseline_image)
    cv2.imwrite(current_path, current_image_with_20px_change)

    return baseline_path, current_path
