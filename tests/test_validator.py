import pytest
import numpy as np
import os
from visual_diff.validator import validate_image_file, validate_dimensions


class TestValidator:
    def test_missing_file_error(self):
        """Test that missing file raises an error with clear message."""
        with pytest.raises(FileNotFoundError):
            validate_image_file("/nonexistent/path/image.png", "baseline")

    def test_invalid_image_error(self, temp_output_dir):
        """Test that invalid image file raises an error."""
        invalid_file = os.path.join(temp_output_dir, "invalid.png")
        with open(invalid_file, "w") as f:
            f.write("not an image")

        with pytest.raises(ValueError):
            validate_image_file(invalid_file, "baseline")

    def test_dimension_mismatch_error_message(self, baseline_image, current_image_with_large_change, temp_output_dir):
        """Test that dimension mismatch error contains both dimensions."""
        import cv2

        baseline_path = os.path.join(temp_output_dir, "baseline.png")
        current_path = os.path.join(temp_output_dir, "current.png")

        img1 = np.ones((100, 100, 3), dtype=np.uint8) * 255
        img2 = np.ones((50, 75, 3), dtype=np.uint8) * 255

        cv2.imwrite(baseline_path, img1)
        cv2.imwrite(current_path, img2)

        img1_read = cv2.imread(baseline_path)
        img2_read = cv2.imread(current_path)

        error = None
        try:
            validate_dimensions(img1_read, img2_read)
        except ValueError as e:
            error = str(e)

        assert error is not None
        assert "50" in error or "75" in error
        assert "100" in error
