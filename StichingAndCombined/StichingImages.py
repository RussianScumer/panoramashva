from stitching import AffineStitcher
import cv2
import os
def add_second_part(images):
    if os.path.isfile('second_part.jpg'):
        second_part = cv2.imread('second_part.jpg')
        images.insert(0, second_part)
    return images

def shovStiching(images):
    settings = {
        "confidence_threshold": 0.05
    }

    stitcher = AffineStitcher(blend_strength=20)
    # stitcher = Stitcher(detector="sift", confidence_threshold=0.2)



    if os.path.isfile('second_part.jpg'):
        images = add_second_part(images)
        panorama = stitcher.stitch([*images])
    else:
        panorama = stitcher.stitch([
            *images
        ])

    cv2.imwrite("Panorama1Part.jpg", panorama)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print('done')
# Save panorama
#Panorama1Part
#NewBeginingPanoramaPart1
