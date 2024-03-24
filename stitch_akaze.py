import cv2
import numpy as np
import os

def border_points(transformation, h, w):
    corners = np.array([[0, 0, 1], [0, h, 1], [w, 0, 1], [w, h, 1]])
    transformed_corners = np.dot(transformation, corners.T).T
    transformed_corners /= transformed_corners[:, 2:]
    min_x = int(np.floor(np.min(transformed_corners[:, 0])))
    min_y = int(np.floor(np.min(transformed_corners[:, 1])))
    max_x = int(np.ceil(np.max(transformed_corners[:, 0])))
    max_y = int(np.ceil(np.max(transformed_corners[:, 1])))
    return min_x, min_y, max_x, max_y


def stitch_akaze(videofile,
 kps_detect=1000,
 matches_take=100,
 ransac_threshold=4.0,
 ransac_iters=2000,
 fps=60,
 delay_in_seconds=0.5):
    images, kps, fts = [None]*2, [None]*2, [None]*2
    transformations = [np.eye(3), None]
    status_min_percent = 100
    assert os.path.exists(videofile)
    stream = cv2.VideoCapture(videofile)
    (grabbed, images[0]) = stream.read()
    videothresh = int(fps * delay_in_seconds)
    framecount, totalframecount, pausecount = 0, 0, 0
    descriptor = cv2.AKAZE_create(nOctaves=1, nOctaveLayers=3)
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    (kps[0], fts[0]) = descriptor.detectAndCompute(images[0], mask=None)
    h, w = images[0].shape[:2] # width and height are the same for all images
    ratio, middle_h, middle_w = 0.1, h//2+1, w//2+1
    window_h, window_w = int(h * ratio), int(w * ratio)
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
        (kps[1], fts[1]) = descriptor.detectAndCompute(image1, mask=None)
        matches = matcher.match(fts[1], fts[0])
        matches = sorted(matches, key=lambda x: x.distance)
        #matches.sort(key=lambda x: x.distance)
        matches = matches[:matches_take]
        pts0 = np.array([kps[0][match.trainIdx].pt for match in matches])
        pts1 = np.array([kps[1][match.queryIdx].pt for match in matches])
        affine, status = cv2.findHomography(pts1, pts0, cv2.RANSAC, ransac_threshold)
        if np.count_nonzero(status)/len(status) < status_min_percent:
            status_min_percent = np.count_nonzero(status)/len(status)
        transformations[1] = affine
        min_x, min_y, max_x, max_y = border_points(transformations[0].dot(transformations[1]), *images[1].shape[:2])
        result = cv2.copyMakeBorder(result, max(0, -min_y), max(0, max_y-result.shape[0]),
                                     max(0, -min_x), max(0, max_x-result.shape[1]), cv2.BORDER_CONSTANT, value=(0,0,0))
        shifts = np.array([-min_x, -min_y, max_x-images[0].shape[1], max_y-images[0].shape[0]])
        max_shift_ind = np.argmax(shifts)
        whole_image_left = True
        if shifts[max_shift_ind] > 0:
            whole_image_left = False
        if max_shift_ind == 1:
            image1[middle_h+window_h:, :] = 0
        elif max_shift_ind == 3:
            image1[:middle_h-window_h, :] = 0
        elif max_shift_ind == 0:
            image1[:, middle_w+window_w:] = 0
        elif max_shift_ind == 2:
            image1[:, :middle_w-window_w] = 0
        if whole_image_left:
            continue
        else:
            transformations[1] = transformations[0].dot(transformations[1])
        if min_x < 0 or min_y < 0:
            translation = np.array([[1, 0, max(-min_x, 0)], [0, 1, max(-min_y, 0)], [0, 0, 1]])
            transformations[1] = translation.dot(transformations[1])
        warped = cv2.warpPerspective(image1, transformations[1], (result.shape[1], result.shape[0]))
        warped[warped == 0] = result[warped == 0]
        result = warped
        kps[0], fts[0] = kps[1], fts[1]
        images[0], transformations[0] = images[1], transformations[1]
        if pausecount % 100 == 0:
            cv2.imwrite('results/final_%s.jpg' % pausecount, result)
            result = cv2.medianBlur(result, 3)
    stream.release()
    print('Total frame count: %d' % totalframecount)
    print('Min status percent: %d' % status_min_percent)
    return result

# Использование функции для создания панорамного изображения из видео
videofile = 'videotest2.mp4'  # Укажите путь к вашему видеофайлу
panorama_image = stitch_akaze(videofile)
print(panorama_image)
# Вывод панорамного изображения
cv2.imwrite('PanoramaImage.jpg', panorama_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
