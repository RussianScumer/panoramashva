from math import ceil

import cv2
import time
from pathlib import Path
from joblib import Parallel, delayed
from stitching import Stitcher

from flowvideo import flowvideo
from utils import save_frames_from_vid, find_slices
from stitch_horizontal import combine_images_horizontally

path_to_videos = Path('./videos')  # путь к папке с видео
path_to_frames = Path('./frames')  # путь к папке, куда будут сохраняться кадры
path_to_panos = Path('./panos')  # путь к папке, куда будут сохраняться промежуточные панорамы
path_to_frames.mkdir(exist_ok=True, parents=True)
path_to_panos.mkdir(exist_ok=True, parents=True)

#Сшивать либо до конца алгоритмами, либо последний шаг втупую, зависит от качества видео, тряски и т.п.
how_to_stitch = True

# настройки сшивателя
stitcher_settings = {'try_use_gpu': True,
                     'crop': True,
                     # В конце после склейки обрезает панораму так, чтобы не было чёрных областей по бокам. Если это
                     # не делать, то в следующей итерации панорамы между собой не сошьются нормально
                     'detector': 'sift',
                     # С видом детектора можно экспериментировать, но по моему этот работает лучше всего
                     'match_conf': 0.25,
                     # Если поставить очень высокий конфиденс фичей, склейка часто будет неудачной. Очень низкий тоже
                     # плохо. Можно экспериментировать
                     'range_width': 1,
                     # Эта настройка говорит сшивателю сшивать только последовательные фотки, не перескакивая
                     'adjuster': 'ray',
                     # Штука, которая пробует подбирать правильную гомографию. Эта самая медленная, но самая
                     # правильная в нашем случае
                     'confidence_threshold': 0,
                     # Эта настройка говорит сшивателю сшивать все последовательные фотки, даже если там низкий
                     # конфиденс маппинга
                     'wave_correct_kind': 'horiz',
                     # Вспомогательная корректировка перспективы, выстраиваем горизонтально
                     'final_megapix': -1,  # Разрешение панорамы. -3 означает полное разрешение без сжатия
                     'low_megapix': 0.25,  # Вспомогательный ресайз для этапов сшивателя (лучше посмотреть документацию)
                     'medium_megapix': 0.5,
                     # Вспомогательный ресайз для этапов сшивателя (лучше посмотреть документацию)
                     }


# Комментарий по поводу настроек сшивателя. В теории должны работать аффинные преобразования для этой задачи. Но у
# меня не получилось добиться нормальных результатов. Полагаю из-за тряски, поворотов и искажений камеры. Если бы
# камера была полностью стабильна и без искажений, аффинные преобразования смогли бы полностью хорошо сшить всю
# деталь как будто бы её по частям отсканировали сканером (в теории)

def get_pano_for_slice(start, end, n, step):
    # Основная функция, которая берёт индексы начального кадра и конечного и сшивает их в панораму. n и step просто
    # порядковые номера панорамы в цикле, так как я распараллелил её через joblib Само сшивание может падать,
    # когда не находит проавильные параметры камеры для текущих фичей. Но так как сами фичи при каждом запуске
    # меняются, потому что этот процесс вероятностный, то я сделал бесконечные попытки сшивки, пока не сошьётся Лучше
    # конечно воткнуть счётчик попыток и после 10-15 попыток всё же выбивать ошибку, чтобы не зависло насовсем
    success = False
    while not success:
        time_start = time.time()
        try:
            stitcher = Stitcher(
                **stitcher_settings)  # Здесь каждый раз создаём stitcher, чтобы иметь возможность запускать
            # параллельно через joblib. Сам объект stitcher нельзя таскать в параллельных процессах.
            panorama = stitcher.stitch(images[
                                       start:end])  # Здесь images это глобальный список кадров. Оставил так, чтобы
            # не забивать оперативку в параллельных процессах, иначе в списке параметров каждый раз будет ещё и
            # список фоток, который может много занимать
            cv2.imwrite(f'./panos/{step}_{n}.jpg', panorama)  # Сохраняет промежуточную панораму на диск
            print(f'Done')
            success = True
            time_end = time.time() - time_start
            print(f'Done in {time_end} seconds')
            return panorama
        except Exception as e:
            print(e)
            time_end = time.time() - time_start
            print(f'failed after {time_end} seconds, trying again')


if __name__ == '__main__':
    vid_name = '1'  # Здесь название видео, которое надо разбить на кадры
    vid_name = vid_name + '.mp4'
    vid_frames_folder = Path(path_to_frames, f'{vid_name.split(".")[0]}')
    vid_frames_folder.mkdir(exist_ok=True, parents=True)
    vid_path = Path(path_to_videos, vid_name).as_posix()
    save_frames_from_vid(vid_path, vid_frames_folder, every_count=100)  # Разбиваем видео на кадры
    what_flow = flowvideo(vid_name)
    # Создаём список кадров, из которых надо сшить панораму
    images = []
    # Очень важно отсортировать по номеру кадра, чтобы они шли подряд. Оригинальная сортировка делает это неправильно
    # (Например 3, 10, 2. Вместо 3, 2, 10)
    for img_path in sorted(vid_frames_folder.glob('*.jpg'), key=lambda x: int(x.stem)):
        img = cv2.imread(img_path.as_posix())
        if what_flow:
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Очень важно повернуть кадры, чтобы они сшивальсь
        # слева-направо. Вертикально работает очень плохо или не работает вообще
        images.append(img)
    print(len(images))

    step = 1  # Начальный шаг
    overlap = 5  # Перехлёст количества фото. Место для экспериментов
    num_to_stich = 10  # Количество склеиваемых фото. Чем больше, тем квадратично дольше ждать и менее стабильно. 10
    steps_to_do = len(images)
    tmp = 0
    while steps_to_do > 1:
        tmp = steps_to_do
        #print(tmp)
        steps_to_do = int(ceil(steps_to_do / num_to_stich))
    steps_to_do = tmp
    print(steps_to_do)
    # практически оптимально.
    while len(images) > num_to_stich + 5:  # Склеиваем рекурсивно, пока не останется фоток на одну склейку
        print(f'------Step {step}------')
        if step == steps_to_do - 1 and how_to_stitch:
            overlap = num_to_stich
        if len(images) < num_to_stich + 5:
            num_to_stich = len(images)

        slices = find_slices(len(images), num_to_stich, overlap)
        print(f'{len(slices)} slices')
        print(slices)

        params = [(start, end, n, step) for n, (start, end) in enumerate(slices)]
        res = Parallel(n_jobs=12)(delayed(get_pano_for_slice)(*param) for param in
                                  params)  # Параллельно склеиваем панорамы, чтоб не ждать долго. n_jobs под себя
        # настраиваем
        images = res.copy()
        print(f'{len(images)} images left')
        step += 1
    print('Done')

    # Здесь не очень хорошее решение с точки зрения архитектуры, но я не запаривался, а делал, чтоб побыстрее.
    # Надо просто повторить ещё одну склейку, но немного с другими параметрами
    if how_to_stitch:
        combine_images_horizontally('panos', 'copythere', step - 1)
    else:
        stitcher_settings.update({'crop': False,
                                  # Из-за больших искажений, сшиватель просто не сможет найти общую область, поэтому
                                  # оставляем чёрные полосы
                                  'final_megapix': 3, })  # панорама ограничена примерно 32000 пикселей по ширине/высоте.
        # Последняя склейка делает это число больше, поэтому приходится делать сжатие, нельзя оставлять -3

        final_pano = get_pano_for_slice(start=0, end=len(images) + 3, n=0, step=999)
