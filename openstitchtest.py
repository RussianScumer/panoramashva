import os

import cv2
from stitching import Stitcher
from stitching import AffineStitcher

settings = {"detector": "sift", "confidence_threshold": 0.2, "try_use_gpu": True}
stitcher = Stitcher(**settings)
settingsAffine = {"confidence_threshold": 0.2, "try_use_gpu": True}
stitcherAffine = AffineStitcher()
'''
imagelast = 0
vidcap = cv2.VideoCapture('videotest7.mp4')
success, image = vidcap.read()
count = 0
images = []
dim = (480, 640)
videothresh = 30
framecount = 0
image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
images.append(image)
while success:
    # cv2.imwrite("frame%d.jpg" % count, image)  # save frame as JPEG file
    success, image = vidcap.read()
    framecount += 1
    if image is not None:
        imagelast = image
    if framecount == videothresh:
        framecount = 0
    else:
        continue
    if image is not None:
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        #image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        images.append(image)
    print('Read a new frame: ', success)
    count += 1
#print(imagelast)
imagelast = cv2.resize(imagelast, dim, interpolation=cv2.INTER_AREA)
images.append(imagelast)
print(count + 2)
'''


def get_all_file_names(directory):
    file_names = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_names.append(os.path.join(root, file))
    return file_names


directory_path = 'key_frames'
all_files = get_all_file_names(directory_path)
all_files = sorted(all_files, key=lambda x: int(x.split('frame')[-1].split('.')[0]))
print(all_files)
#panorama = stitcher.stitch(all_files)
#panorama = stitcher.stitch(['key_frames/frame0.jpg', 'key_frames/frame1.jpg'])
panorama = stitcherAffine.stitch(all_files)
# panorama = cv2.resize(panorama, dim, interpolation=cv2.INTER_AREA)
cv2.imshow('Panorama', panorama)
cv2.imwrite('panorama.jpg', panorama)
cv2.waitKey()
cv2.destroyAllWindows()
