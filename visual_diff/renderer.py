import cv2
import os


def render_differences(current_image_path, differences, output_folder):
    """
    Draw red rectangles on a copy of the current image.
    Output is saved to output_folder/output.png.
    Original image is never modified.
    """
    os.makedirs(output_folder, exist_ok=True)

    img = cv2.imread(current_image_path)
    output_img = img.copy()

    for diff in differences:
        x, y, w, h = diff["x"], diff["y"], diff["w"], diff["h"]
        cv2.rectangle(output_img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    output_path = os.path.join(output_folder, "output.png")
    cv2.imwrite(output_path, output_img)
