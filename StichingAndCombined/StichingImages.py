from stitching import AffineStitcher
import cv2
import os

stitcher = AffineStitcher()


def add_second_part(images):
    if os.path.isfile('second_part.png'):
        second_part = 'second_part.png'
        images.insert(0, second_part)
    return images

def stitch_with_second_part(images):
    print("2raz")
    print(f"Объединено {len(images)} изображений")
    images = add_second_part(images)
    print(images)
    panorama = stitcher.stitch([*images])
    return panorama

def stitch_without_second_part(images):
    print("1raz")
    print(f"Объединено {len(images)} изображений")
    print(images)
    panorama = stitcher.stitch([*images])
    return panorama

def shovStiching(images):
    panorama = None
    try:
        # if os.path.isfile('second_part.png'):
        #     panorama = stitch_with_second_part(images)
        # if not os.path.isfile('second_part.png'):
        panorama = stitch_without_second_part(images)

        cv2.imwrite("Panorama1Part.png", panorama)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print('done')

    except FileNotFoundError:
        print("Ошибка: Файл 'second_part.png' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при stitching: {e}")
# Save panorama
#Panorama1Part
#NewBeginingPanoramaPart1

 # if os.path.isfile('second_part.png'):
    #     print("2raz")
    #     print(f"Объединено {len(images)} изображений")
    #     add_second_part(images)
    #     print((images))
    #     panorama = stitcher.stitch([*images])
    # else:
    #     print("1raz")
    #     print(f"Объединено {len(images)} изображений")
    #     panorama = stitcher.stitch([
    #         *images
    #     ])
