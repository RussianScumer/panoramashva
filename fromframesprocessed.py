import numpy as np
from PIL import Image
from ClearDirectory import delete_files_in_folder
import os 
import cv2
#kadri v papku frames/...
def stitch_fromframesprocessed(path_to_frames='4',need_to_resize=True,
                     need_to_clear_folder=True):
    folder_path = "frames/%s" % path_to_frames
    if need_to_clear_folder:
        delete_files_in_folder(folder_path)
    file_list = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    file_list = sorted(file_list, key=lambda x: int(x.split('frame')[-1].split('.')[0]))
    print(file_list)

    photo_array = []
    # собираем все в один np array
    for file in file_list:
        file_path = os.path.join(folder_path, file)
        img = Image.open(file_path)
        img_array = np.array(img)
        photo_array.append(img_array)

    print(photo_array)
    photo_array = np.array(photo_array)
    # склейка
    photo_array = np.concatenate(photo_array, axis=0)
    photo_array = cv2.cvtColor(photo_array, cv2.COLOR_BGR2RGB)
    if need_to_resize:
        cv2.imwrite('results/' + path_to_frames + '_resized' + '.png', photo_array)
    else:
        cv2.imwrite('results/' + path_to_frames + '.png', photo_array)
    # cv2.imshow('test', photo_array)
    print("done")
    #cv2.waitKey()
