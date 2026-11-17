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
