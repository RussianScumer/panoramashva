import os

import cv2

# target folder
folder = "frames/"

# load images
filenames = os.listdir(folder)
images = [];
for file in filenames:
    # get image
    img = cv2.imread(folder + file)

    # save
    images.append(img)

# use built in stitcher
stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)
status, stitched = stitcher.stitch(images)
if status == cv2.Stitcher_OK:
    cv2.imshow('Panorama', stitched)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Error during stitching:", status)
cv2.imwrite("Stitched.jpg", stitched)
cv2.waitKey(0)