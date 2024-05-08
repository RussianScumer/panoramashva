import os
import cv2

image_folder = r'H:\panoramashva\panoramashva\Test'
def get_images(directory):
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        return []

    images = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img_path = os.path.join(directory, filename)
            image = cv2.imread(img_path)

            images.append(image)
            if len(images) == 2:
                break
    return images

get_images(image_folder)

