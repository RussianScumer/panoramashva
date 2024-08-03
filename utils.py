import cv2
from pathlib import Path


def save_frames_from_vid(vid_path, save_path, every_count=100):
    # Берёт видео и сохраняет каждый every_count кадр, включая первый и последний Я брал каждый 100-й кадр,
    # работает неплохо. Можно попробовать увеличить до 150, чтобы получить меньше склеек на целое видео
    vid = cv2.VideoCapture(vid_path)
    while True:
        status, frame = vid.read()
        counter = vid.get(cv2.CAP_PROP_POS_FRAMES)
        if counter == 1 or counter % every_count == 0 or counter == int(vid.get(cv2.CAP_PROP_FRAME_COUNT)):
            if frame is not None:
                cv2.imwrite(Path(save_path, f'{int(counter)}.jpg').as_posix(), frame)
                print(f'Frame {int(counter)}.jpg saved')
            else:
                break
        elif not status:
            break
        else:
            continue


def save_frames_from_vid_40sec(vid_path, save_path, every_count=100):
    # Берёт видео и сохраняет каждый every_count кадр, включая первый и последний
    # Я брал каждый 100-й кадр, работает неплохо. Можно попробовать увеличить до 150, чтобы получить меньше склеек на целое видео
    vid = cv2.VideoCapture(vid_path)
    for i in range(0, 1000):
        status, frame = vid.read()
        counter = vid.get(cv2.CAP_PROP_POS_FRAMES)
        if counter == 1 or counter % every_count == 0 or counter == int(vid.get(cv2.CAP_PROP_FRAME_COUNT)):
            if frame is not None:
                cv2.imwrite(Path(save_path, f'{int(counter)}.jpg').as_posix(), frame)
                print(f'Frame {int(counter)}.jpg saved')
            else:
                break
        elif not status:
            break
        else:
            continue

def find_slices(list_len, window_size, step=5):
    # Разбивает всё количество фоток на равные части размера window_size (стабильнее всего 10 штук) с перехлёстом по
    # step штук, для (10, 5) работает
    slices = [(i, i + window_size) for i in range(0, list_len, step)]
    if slices[-1][1] == list_len:
        slices[-1] = (slices[-1][0], slices[-1][1] + 1)
    elif slices[-2][1] == list_len:
        del slices[-1]
        slices[-1] = (slices[-1][0], slices[-1][1] + 1)
    elif slices[-2][1] > list_len:
        del slices[-1]
    return slices

def count_iterations(total_images, num_to_stitch):
    images = list(range(total_images))
    iterations = 0

    def stitch_images(images, num_to_stitch):
        nonlocal iterations
        while len(images) > num_to_stitch:
            iterations += 1
            new_images = []
            for i in range(0, len(images) - num_to_stitch + 1, 5):
                new_images.append(images[i:i+num_to_stitch])
            images = new_images
        return images

    stitch_images(images, num_to_stitch)
    return iterations
