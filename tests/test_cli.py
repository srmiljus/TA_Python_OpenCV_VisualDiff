import pytest
import sys
import subprocess


class TestCLI:
    def test_exit_code_0_when_images_identical(self, identical_images_files, temp_output_dir):
        """Test exit code 0 and output when images are identical (requirement 7)."""
        baseline_path, current_path = identical_images_files

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "visual_diff.cli",
                baseline_path,
                current_path,
                temp_output_dir,
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, "Exit code should be 0 when no differences found"
        assert "Differences found: 0" in result.stdout, "stdout should show 'Differences found: 0'"

    def test_exit_code_1_when_differences_found(self, images_with_two_changes_files, temp_output_dir):
        """Test exit code 1 and output when differences are found (requirement 7)."""
        baseline_path, current_path = images_with_two_changes_files

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "visual_diff.cli",
                baseline_path,
                current_path,
                temp_output_dir,
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1, "Exit code should be 1 when differences found"
        assert "Differences found: 2" in result.stdout, "stdout should show 'Differences found: 2'"

    def test_exit_code_2_when_file_missing(self, temp_output_dir):
        """Test exit code 2 and error message when file is missing (requirement 2 & 7)."""
        nonexistent_baseline = "/nonexistent/baseline.png"
        current_path = "/nonexistent/current.png"

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "visual_diff.cli",
                nonexistent_baseline,
                current_path,
                temp_output_dir,
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 2, "Exit code should be 2 when file is missing"
        assert nonexistent_baseline in result.stderr, "stderr should contain missing file path"

    def test_exit_code_2_when_dimensions_differ(self, images_different_dimensions_files, temp_output_dir):
        """Test exit code 2 and dimension error when images have different sizes (requirement 2 & 7)."""
        baseline_path, current_path = images_different_dimensions_files

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "visual_diff.cli",
                baseline_path,
                current_path,
                temp_output_dir,
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 2, "Exit code should be 2 when dimensions differ"
        output = result.stderr
        assert "100" in output and ("50" in output or "75" in output), "stderr should contain both image dimensions"

    def test_custom_threshold_argument(self, images_with_20px_change_files, temp_output_dir):
        """Test that --threshold argument works (requirement 1 & 4)."""
        baseline_path, current_path = images_with_20px_change_files

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "visual_diff.cli",
                baseline_path,
                current_path,
                temp_output_dir,
                "--threshold",
                "50",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, "Exit code should be 0 when change is below threshold"
        assert "Differences found: 0" in result.stdout, "stdout should show 'Differences found: 0'"

    def test_cli_saves_output_image(self, images_with_two_changes_files, temp_output_dir):
        """Test that CLI creates output folder if missing and saves output image (requirement 5)."""
        import os
        import cv2

        baseline_path, current_path = images_with_two_changes_files
        new_output_dir = os.path.join(temp_output_dir, "new_output")

        assert not os.path.exists(new_output_dir), "new_output folder should not exist before CLI runs"

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "visual_diff.cli",
                baseline_path,
                current_path,
                new_output_dir,
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1, "Exit code should be 1 when differences found"

        assert os.path.exists(new_output_dir), "Output folder should be created"

        png_files = [f for f in os.listdir(new_output_dir) if f.endswith(".png")]
        assert len(png_files) == 1, "Exactly one .png file should be created in output folder"

        output_image_path = os.path.join(new_output_dir, png_files[0])
        output_img = cv2.imread(output_image_path)
        current_img = cv2.imread(current_path)

        assert output_img is not None, "Output image should be readable"
        assert output_img.shape == current_img.shape, "Output image should have same dimensions as current image"
