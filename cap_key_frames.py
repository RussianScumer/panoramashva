import os

import cv2
import numpy as np
import argparse


def main(videofile):
    # Construct VideoCapture object to get frame-by-frame stream
    vid_cap = cv2.VideoCapture(videofile)

    # SIFT descriptors are utilized to describe the overlapping between the
    # current frame and its neighbor
    sift = cv2.AKAZE.create()

    # The first key frame (frame0.jpg) is selected by default
    success, last = vid_cap.read()
    w = last.shape[1]
    h = last.shape[0]
    dim = (int(w * 3 / 10), int(h * 3 / 10))
    last = cv2.resize(last, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite('key_frames/frame0.jpg', last)
    print("Captured frame0.jpg")
    count = 1
    frame_num = 1

    w = int(last.shape[1] * 3 / 3)  # the region to detect matching points
    stride = 10         # stride for accelerating capturing
    min_match_num = 2# minimum number of matches required (to stitch well)
    max_match_num = 600  # maximum number of matches (to avoid redundant frames)

    while success:
        if count % stride == 0:
            # Detect and compute key points and descriptors
            kp1, des1 = sift.detectAndCompute(last[:, -w:], None)
            kp2, des2 = sift.detectAndCompute(image[:, :w], None)

            # Use the Brute-Force matcher to obtain matches
            bf = cv2.BFMatcher(normType=cv2.NORM_L2)  # Using Euclidean distance
            matches = bf.knnMatch(des1, des2, k=2)

            # Define Valid Match: whose distance is less than match_ratio times
            # the distance of the second best nearest neighbor.
            match_ratio = 0.6

            # Pick up valid matches
            valid_matches = []
            for m1, m2 in matches:
                if m1.distance < match_ratio * m2.distance:
                    valid_matches.append(m1)

            # At least 4 points are needed to compute Homography
            if len(valid_matches) > 4:
                img1_pts = []
                img2_pts = []
                for match in valid_matches:
                    img1_pts.append(kp1[match.queryIdx].pt)
                    img2_pts.append(kp2[match.trainIdx].pt)

                # Formalize as matrices (for the sake of computing Homography)
                img1_pts = np.float32(img1_pts).reshape(-1, 1, 2)
                img2_pts = np.float32(img2_pts).reshape(-1, 1, 2)

                # Compute the Homography matrix
                _, mask = cv2.findHomography(img1_pts, img2_pts,
                                             cv2.RANSAC, 10.0)

                if min_match_num < np.count_nonzero(mask) < max_match_num:
                    # Save key frame as JPG file
                    last = image
                    print("Captured frame{}.jpg".format(frame_num))
                    w = last.shape[1]
                    h = last.shape[0]
                    dim = (int(w * 3 / 10), int(h * 3 / 10))
                    last = cv2.resize(last, dim, interpolation=cv2.INTER_AREA)
                    cv2.imwrite('key_frames/frame%d.jpg' % frame_num, last)
                    frame_num += 1
        success, image = vid_cap.read()
        count += 1


def clear_folder(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # если вы хотите удалить также папки, раскомментируйте следующую строку
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)




if __name__ == "__main__":
    #parser = argparse.ArgumentParser()
    #parser.add_argument('file', nargs='?', default='360video.mp4',
                       # help="path of the video file (default: 360video.mp4)")
    #args = parser.parse_args()
    #folder_to_clear = 'путь_к_папке_для_очистки'
    #clear_folder("key_frames")
    main('videotest5.mp4')