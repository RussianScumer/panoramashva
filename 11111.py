import os
import cv2
import numpy as np
import scipy
import imutils


def border_points(transformation, shape1, shape2):
    height, width = shape1, shape2
    corners = np.array([[0, 0, 1], [width, 0, 1], [0, height, 1], [width, height, 1]])

    transformed_corners = np.dot(transformation, corners.T).T

    min_x = np.min(transformed_corners[:, 0])
    min_y = np.min(transformed_corners[:, 1])
    max_x = np.max(transformed_corners[:, 0])
    max_y = np.max(transformed_corners[:, 1])

    return min_x, min_y, max_x, max_y


def stitch_akaze(videofile,
                 kps_detect=1000,  # количество особых точек, которое ищем на кадрах
                 matches_take=100,  # количество соответствий по которым строиться матрица
                 ransac_threshold=4.0,  # пороговое значение для алгоритма Ransac
                 ransac_iters=2000,  # Количество итераций для алгоритма Ransac
                 fps=60,  # Число кадров в секунду
                 delay_in_seconds=0.5):  # интервал извлечения кадров
    images, kps, fts = [None] * 2, [None] * 2, [None] * 2
    print(images)
    transformations = [np.eye(3), None]

    status_min_percent = 100

    assert os.path.exists(videofile)
    stream = cv2.VideoCapture(videofile)
    (grabbed, images[0]) = stream.read()
    videothresh = int(fps * delay_in_seconds)
    framecount, totalframecount, pausecount = 0, 0, 0

    descriptor = cv2.AKAZE.create(nOctaves=1, nOctaveLayers=3, max_points=kps_detect)
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    (kps[0], fts[0]) = descriptor.detectAndCompute(images[0], mask=None)

    h, w = images[0].shape[:2]
    ratio, middle_h, middle_w = 0.1, h // 2 + 1, w // 2 + 1  # ratio возможно и делать размер склеиваемых изображений!!!
    window_h, window_w = int(h * ratio), int(w * ratio)
    print('Centers (h and w): %d %d' % (middle_h, middle_w))
    print('Windows height %s px, width %s ps' % (window_h, window_w))

    result = images[0].copy()
    while grabbed:
        (grabbed, images[1]) = stream.read()
        framecount += 1
        totalframecount += 1
        if framecount == videothresh:
            framecount = 0
        else:
            continue
        pausecount += 1

        image1 = images[1].copy()
        print('\nProcessing %s' % pausecount)

        (kps[1], fts[1]) = descriptor.detectAndCompute(image1, mask=None)
        print('AKAZE: len(kps) %d' % len(kps))

        matches = matcher.match(fts[1], fts[0])
        matches = list(matches)
        print('Total matches num: %d' % len(matches))

        matches.sort(key=lambda x: x.distance)
        matches = matches[:matches_take]
        print('Only %d matches were taken, max distance %f' % (len(matches), matches[-1].distance))
        pts0 = np.array([kps[0][match.trainIdx].pt for match in matches])
        pts1 = np.array([kps[1][match.queryIdx].pt for match in matches])

        affine = None
        affine, status = cv2.findHomography(pts0, pts1, method=cv2.RANSAC, ransacReprojThreshold=ransac_threshold,
                                            maxIters=ransac_iters)
        if np.count_nonzero(status) / len(status) < status_min_percent:
            status_min_percent = np.count_nonzero(status) / len(status)

        # affine = affine.params

        print('affine transformation: \n %s' % affine)

        transformations[1] = affine
        min_x, min_y, max_x, max_y = border_points(transformations[0].dot(transformations[1]), images[1].shape[1],
                                                   images[1].shape[0])
        print('Borders: min_x %s (0) min_y %s (0) max_x %s (%s) max_y %s ( % s) ' % (
            min_x, min_y, max_x, result.shape[1], max_y, result.shape[0]))
        result = cv2.copyMakeBorder(result, int(max(0, -min_y)), int(max(0, max_y - result.shape[0])),
                                    int(max(0, -min_x)), int(max(0, max_x - result.shape[1])), cv2.BORDER_CONSTANT,
                                    value=(0, 0, 0))

        _min_x, _min_y, _max_x, _max_y = border_points(transformations[0].dot(transformations[1]), images[1].shape[1],
                                                       images[1].shape[0])
        shifts = np.array([-_min_x, -_min_y, _max_x - images[0].shape[1], _max_y - images[0].shape[0]])
        max_shift_ind = np.argmax(shifts)
        whole_image_left = True
        if shifts[max_shift_ind] > 0:
            whole_image_left = False
            if max_shift_ind == 1:
                image1[middle_h + window_h:, :] = 0
            elif max_shift_ind == 3:
                image1[:middle_h - window_h, :] = 0
            elif max_shift_ind == 0:
                image1[:, middle_w + window_w:] = 0
            elif max_shift_ind == 2:
                image1[:, :middle_w - window_w] = 0
        if whole_image_left:
            continue
        else:
            transformations[1] = transformations[0].dot(transformations[1])
        if min_x < 0 or min_y < 0:
            translation = np.array([[1, 0, max(-min_x, 0)], [0, 1, max(-min_y, 0)], [0, 0, 1]])
            transformations[1] = translation.dot(transformations[1])
        warped = cv2.warpPerspective(image1, transformations[1], (result.shape[1], result.shape[0]), result.copy(),
                                     borderMode=cv2.BORDER_TRANSPARENT)
        warped[warped == 0] = result[warped == 0]
        result = warped
        kps[0], fts[0] = kps[1], fts[1]
        images[0], transformations[0] = images[1], transformations[1]
        if pausecount % 100 == 0:
            temp = imutils.resize(result, height=min(800, result.shape[1]))
            # cv2.imshow(str(pausecount), temp)
            # cv2.waitKey(0)
            # cv2.imwrite('results/final_%s.jpg' % pausecount, result)
        filename = 'frames/final_panorama.jpg'
        # cv2.imwrite(filename, result)
        # print(f"Panorama saved as {filename}")
    result = cv2.medianBlur(result, 3)
    stream.release()
    print('Total frame count: %d' % totalframecount)
    print('Min status percent: %d' % status_min_percent)
    return result


'''
resultfinal = stitch_akaze(videofile='videotest2.mp4',
             kps_detect=5000,  # количество особых точек, которое ищем на кадрах
             matches_take=2000,  # количество соответствий по которым строиться матрица
             ransac_threshold=8.0,  # пороговое значение для алгоритма Ransac
             ransac_iters=2000,  # Количество итераций для алгоритма Ransac
             fps=30,  # Число кадров в секунду
             delay_in_seconds=0.5)
#cv2.imwrite('resultfinal2.jpg', resultfinal)
'''


imagelast = 0
vidcap = cv2.VideoCapture('videotest4.mp4')
success, image = vidcap.read()
count = 0
images = []
images.append(image)
dim = (480, 320)
videothresh = 30
framecount = 0
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
images.append(imagelast)

stitcher = cv2.Stitcher.create()
ret, pano = stitcher.stitch(images)

if ret == cv2.STITCHER_OK:
    cv2.imshow('Panorama', pano)
    cv2.imwrite('panorama.jpg', pano)
    cv2.waitKey()
    cv2.destroyAllWindows()
else:
    print("Error during Stitching")
