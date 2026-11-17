import argparse
import sys
from visual_diff.validator import validate_image_file, validate_dimensions
from visual_diff.comparator import find_differences
from visual_diff.renderer import render_differences


def main():
    parser = argparse.ArgumentParser(description="Compare two images and visualize differences")
    parser.add_argument("baseline", help="Path to baseline image")
    parser.add_argument("current", help="Path to current image")
    parser.add_argument("output", help="Output directory for results")
    parser.add_argument("--threshold", type=int, default=10, help="Threshold for difference detection")

    args = parser.parse_args()

    try:
        baseline_img = validate_image_file(args.baseline, "Baseline")
        current_img = validate_image_file(args.current, "Current")

        validate_dimensions(baseline_img, current_img)

        differences = find_differences(baseline_img, current_img, args.threshold)
        render_differences(args.current, differences, args.output)

        count = len(differences)
        print(f"Differences found: {count}")

        sys.exit(0 if count == 0 else 1)
    except (FileNotFoundError, ValueError) as e:
        print(str(e), file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
