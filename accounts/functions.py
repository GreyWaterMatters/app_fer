import numpy as np
import cv2
import base64


def preprocess_image(image):
    image_np = np.fromstring(image, np.uint8)
    image_cv = cv2.imdecode(image_np, cv2.IMREAD_UNCHANGED)

    if image_cv.shape[-1] == 3:
        image_gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    else:
        image_gray = image_cv

    dir_cascade_files = r"/home/greywater/Documents/Kirae/app/src/model/.opencv/haarcascades/"
    cascade_file = dir_cascade_files + "haarcascade_frontalface_alt2.xml"
    print(cascade_file)
    cascade = cv2.CascadeClassifier(cascade_file)

    faces = cascade.detectMultiScale(
        image_gray,
        scaleFactor=1.1,
        minNeighbors=1,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    if len(faces) == 1:
        for (x, y, w, h) in faces:
            image_rect = cv2.rectangle(image_cv, (x, y), (x+w, y+h), (255, 0, 0), 2)

            face_image = image_gray[y:y + h, x:x + w]
            image_face_cv = cv2.resize(face_image, (64, 64))
            image_enhanced = cv2.equalizeHist(image_face_cv)
            image_chan = image_enhanced.reshape(1, 64, 64, 1)

    return image_chan, image_rect
