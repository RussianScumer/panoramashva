from stitching import AffineStitcher
import cv2
import os

def shovStiching(images):
    settings = {
        "confidence_threshold": 0.05}

    stitcher = AffineStitcher(blend_strength=20)
    #stitcher = Stitcher(detector="sift", confidence_threshold=0.2)

    if os.path.isfile('second_part.jpg'):
        panorama = stitcher.stitch([
        "second_part.jpg",images
    ])
    else:
        panorama = stitcher.stitch([
       images
    ])
    #Panorama1Part передаем для склейки в StichImageVerticale.
    cv2.imwrite("Panorama1Part.jpg", panorama)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print('done');

# Save panorama
#Panorama1Part
#NewBeginingPanoramaPart1
