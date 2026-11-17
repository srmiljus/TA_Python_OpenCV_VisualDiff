import pytest
import numpy as np
from visual_diff.comparator import find_differences


class TestComparator:
    def test_identical_images_have_no_differences(self, identical_image):
        """Test that identical images produce no differences."""
        result = find_differences(identical_image, identical_image)
        assert result == [] or len(result) == 0

    def test_threshold_filtering(self, baseline_image, current_image_with_small_change):
        """Test that differences below threshold (10 pixels) are filtered out."""
        result = find_differences(baseline_image, current_image_with_small_change, threshold=10)
        assert result == [] or len(result) == 0

    def test_default_threshold_is_10(self, baseline_image, current_image_with_small_change):
        """Test that default threshold is 10 pixels."""
        result = find_differences(baseline_image, current_image_with_small_change)
        assert result == [] or len(result) == 0

    def test_two_separate_changes_give_two_regions(self, baseline_image, current_image_with_two_changes):
        """Test that two separate differences produce two distinct regions."""
        result = find_differences(baseline_image, current_image_with_two_changes, threshold=5)
        assert len(result) == 2

    def test_thin_line_change_is_detected(self, baseline_image, current_image_with_thin_line):
        """Test that thin line changes (1x100 px = 100 px) are detected with default threshold 10."""
        result = find_differences(baseline_image, current_image_with_thin_line, threshold=10)
        assert len(result) == 1, "Thin line with 100 pixels should be detected (100 >= 10)"

    def test_threshold_uses_pixel_count(self, baseline_image, current_image_with_5x4_block):
        """Test that threshold is based on pixel count, not contourArea (5x4 = 20 px)."""
        result = find_differences(baseline_image, current_image_with_5x4_block, threshold=15)
        assert len(result) == 1, "5x4 block with 20 pixels should be detected (20 >= 15)"

    def test_pixel_count_excludes_other_regions(self, images_with_overlapping_regions_files):
        """Test that pixel counting for each region excludes overlapping bounding boxes."""
        import cv2
        baseline_path, current_path = images_with_overlapping_regions_files

        baseline = cv2.imread(baseline_path)
        current = cv2.imread(current_path)

        result = find_differences(baseline, current, threshold=30)

        assert len(result) == 1, "Only vertical line (100 px) should be detected, not U (27 px)"
        assert result[0]["w"] == 1, "Vertical line should have width 1"
