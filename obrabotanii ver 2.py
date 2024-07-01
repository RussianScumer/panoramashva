import cv2
import numpy as np


def crop_center_one_third_height(image_path):
    image = cv2.imread(image_path)

    height, width = image.shape[:2]
    one_third_height = height // 3

    top = one_third_height
    bottom = 2 * one_third_height
    left = 0
    right = width

    cropped_image = image[top:bottom, left:right]
    cv2.imshow('Cropped Image', cropped_image)
    cv2.imwrite('cropped_image.jpg', cropped_image)

# Пример использования функции
image_path = 'Test/frame0.jpg'
crop_center_one_third_height(image_path)
cv2.waitKey(0)
cv2.destroyAllWindows()