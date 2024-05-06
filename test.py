import os
import cv2
from stitching import Stitcher
from stitching import AffineStitcher
from openstitchtest import get_all_file_names

settingsAffine = {"detector": "sift", "confidence_threshold": 0.1}
stitcherAffine = AffineStitcher(**settingsAffine)
directory_path = 'panoramaparts'
all_files = get_all_file_names(directory_path)
all_files = sorted(all_files, key=lambda x: int(x.split('frame')[-1].split('.')[0]))
print(all_files)
panorama = stitcherAffine.stitch(all_files)

cv2.imshow('panorama', panorama)
cv2.waitKey()
cv2.destroyAllWindows()