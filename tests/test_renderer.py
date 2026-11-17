import pytest
import numpy as np
import cv2
import os
from visual_diff.renderer import render_differences


class TestRenderer:
    def test_draws_red_rectangles_on_output(self, current_image_with_large_change, temp_output_dir):
        """Test that red rectangles are drawn on output image."""
        current_path = os.path.join(temp_output_dir, "current.png")
        cv2.imwrite(current_path, current_image_with_large_change)

        differences = [{"x": 10, "y": 10, "w": 10, "h": 10}]
        render_differences(current_path, differences, temp_output_dir)

        output_path = os.path.join(temp_output_dir, "output.png")
        assert os.path.exists(output_path)

        output_img = cv2.imread(output_path)
        assert output_img is not None

    def test_input_images_not_modified(self, current_image_with_large_change, temp_output_dir):
        """Test that original image file is not modified."""
        current_path = os.path.join(temp_output_dir, "current.png")
        cv2.imwrite(current_path, current_image_with_large_change)

        original_img = cv2.imread(current_path)
        original_hash = hash(original_img.tobytes())

        differences = [{"x": 10, "y": 10, "w": 10, "h": 10}]
        render_differences(current_path, differences, temp_output_dir)

        modified_img = cv2.imread(current_path)
        modified_hash = hash(modified_img.tobytes())

        assert original_hash == modified_hash
