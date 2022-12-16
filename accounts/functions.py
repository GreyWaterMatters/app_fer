import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image

from tensorflow.keras.models import load_model

emotions = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}


def decode_base64(data):
    out = base64.decodebytes(data.split(",")[1].encode())
    return out


def encode_base64(data):
    return 'data:image/png;base64,' + data


def get_image_webcam(data):
    decode = decode_base64(data)
    result = preprocess_image(decode)

    font = cv2.FONT_HERSHEY_SIMPLEX
    textsize = cv2.getTextSize(result[0], font, 1, 2)[0]
    textX = (result[1].shape[1] - textsize[0]) / 2
    textY = (result[1].shape[0] + textsize[1]) / 2
    cv2.putText(result[1], result[0], (int(textX), int(textY)), font, 1, (0, 255, 0), 2)

    buffer = BytesIO()
    img = Image.fromarray(result[1])

    img.save(buffer, format="png")
    encoded_string = base64.b64encode(buffer.getvalue()).decode('ascii')

    return encode_base64(encoded_string)


def preprocess_image(image):
    image_np = np.fromstring(image, np.uint8)
    image_cv = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    if len(image_cv.shape) == 2 or image_cv.shape[-1] == 1:
        image_gray = image_cv
    else:
        image_gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    dir_cascade_files = r"/home/greywater/Documents/Kirae/app/src/model/.opencv/haarcascades/"
    cascade_file = dir_cascade_files + "haarcascade_frontalface_alt2.xml"
    cascade = cv2.CascadeClassifier(cascade_file)

    faces = cascade.detectMultiScale(
        image_gray,
        scaleFactor=1.1,
        minNeighbors=1,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    if len(faces) >= 1:

        model = load_model("/home/greywater/Documents/Kirae/app/src/model/model_feat_ex_3_contrast_detect_face")

        for (x, y, w, h) in faces:
            image_rect = cv2.rectangle(image_cv, (x, y), (x+w, y+h), (255, 0, 0), 2)

            face_image = image_gray[y:y + h, x:x + w]
            image_face_cv = cv2.resize(face_image, (64, 64))
            image_enhanced = cv2.equalizeHist(image_face_cv)
            image_chan = image_enhanced.reshape(1, 64, 64, 1)

            prediction = np.argmax(model.predict(image_chan), axis=1)[0]

        return emotions[prediction], image_rect
    else:
        text = "No face detected"
        return text, image_cv



