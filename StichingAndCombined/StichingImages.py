from stitching import AffineStitcher
import cv2
import os
def add_second_part(images):
    if os.path.isfile('second_part.png'):
        second_part = 'second_part.png'
        images.insert(0, second_part)
    return images

def shovStiching(images):
    settings = {
        "confidence_threshold": 0.05
    }

    stitcher = AffineStitcher(blend_strength=20)
    # stitcher = Stitcher(detector="sift", confidence_threshold=0.2)
    if os.path.isfile('second_part.png'):
        print("2raz")
        print(f"Объединено {len(images)} изображений")
        add_second_part(images)
        print((images))
        panorama = stitcher.stitch([*images])
    else:
        print("1raz")
        print(f"Объединено {len(images)} изображений")
        panorama = stitcher.stitch([
            *images
        ])

    cv2.imwrite("Panorama1Part.png", panorama)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print('done')
# Save panorama
#Panorama1Part
#NewBeginingPanoramaPart1
