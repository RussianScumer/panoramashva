import cv2

imagelast = 0
vidcap = cv2.VideoCapture('obrab.mp4')
success, image = vidcap.read()
count = 0
dim = (480, 640)
videothresh = 120
framecount = 0
image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
cv2.imwrite("test/frame%d.jpg" % count, image)
#images.append(image)
while success:
    cv2.imwrite("test/frame%d.jpg" % count, image)  # save frame as JPEG file
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
        #images.append(image)
    print('Read a new frame: ', success)
    count += 1
#print(imagelast)
imagelast = cv2.resize(imagelast, dim, interpolation=cv2.INTER_AREA)
count += 2
#cv2.imwrite("test/frame%d.jpg" % count, image)
#images.append(imagelast)
print(count + 2)
