TA_Python_OpenCV_VisualDiff

A command-line tool that compares two screenshots (baseline and current), finds every region that changed, and saves a copy of the current screenshot with each difference outlined by a red rectangle.

Built with Python, OpenCV and pytest, following a strict test-first (TDD) workflow.

Features
Compares two PNG images pixel by pixel
Groups changed pixels into separate regions (8-connectivity)
Ignores regions smaller than a configurable threshold (exact count of changed pixels)
Saves an annotated copy of the current image with red boxes around each difference
Never modifies the input images
Clear error messages for missing files, invalid images and mismatched dimensions
CI-friendly exit codes
Requirements
Python 3.11+
Dependencies listed in requirements.txt (opencv-python, numpy, pytest, pytest-cov)
Setup

Windows:

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

macOS / Linux:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Usage
python -m visual_diff.cli <baseline.png> <current.png> <output_folder> [--threshold N]
Argument	Description
baseline	Path to the reference screenshot
current	Path to the screenshot to compare
output	Folder for the annotated image (created if it does not exist)
--threshold	Minimum number of changed pixels for a region to count as a difference (default: 10)

Example:

python -m visual_diff.cli baseline.png current.png output --threshold 20

Output:

Differences found: 2

The annotated image is saved to the output folder.

Exit codes
Code	Meaning
0	No differences found
1	Differences found
2	Error (missing file, invalid image, different dimensions)

This makes the tool usable as a CI step: a non-zero exit code fails the pipeline.

How it works
Computes the absolute per-pixel difference between the two images (cv2.absdiff)
Converts the difference to grayscale and marks every changed pixel
Groups changed pixels into connected regions (cv2.connectedComponentsWithStats)
Keeps only regions whose pixel count is at or above the threshold
Draws a red bounding box around each remaining region on a copy of the current image
Running the tests
python -m pytest -v

The suite contains 18 tests covering validation, comparison, rendering and the CLI. All test images are generated with numpy, so no real screenshots are needed.

Project structure
visual_diff/
  cli.py          # argument parsing, exit codes, output message
  validator.py    # file and dimension validation
  comparator.py   # difference detection and threshold filtering
  renderer.py     # draws red rectangles and saves the output image
tests/
  conftest.py     # fixtures that generate test images
  test_cli.py
  test_comparator.py
  test_renderer.py
  test_validator.py
CLAUDE.md         # project rules for the AI coding agent
Development process

The project was built test-first with an AI coding agent (Claude Code), with the commit history reflecting each stage:

RED: requirements written first, then tests derived only from those requirements; every test confirmed to fail before any implementation existed
GREEN: implementation written until all tests passed, without modifying the tests
Bug fixes: each bug found during manual testing was first reproduced with a new failing test, then fixed:
output folder was not created when it did not exist
threshold used contour area instead of the real pixel count, so thin lines were ignored and nearby regions affected each other's counts
Known limitations
Any pixel difference counts as a change, so anti-aliasing or rendering noise between two screenshots can produce small false differences; raise --threshold to filter them out
On Windows, file paths containing non-ASCII characters (for example š, č, ž) are not supported by OpenCV's file reading and writing functions
Both images must have exactly the same dimensions
