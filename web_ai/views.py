import cv2
import time
import numpy as np

from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from tensorflow.keras.models import load_model


emotions = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}


def gen(camera):
    last_prediction = time.time()
    model = load_model("/home/greywater/Documents/Kirae/app/src/model/model_vgg13")

    while True:
        ret, img = camera.read()
        img_bytes = cv2.imencode('.jpg', img)[1].tobytes()

        image_np = np.fromstring(img_bytes, np.uint8)
        image_cv = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        image_gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

        dir_cascade_files = r"/home/greywater/Documents/Kirae/app/src/model/.opencv/haarcascades/"
        cascade_file = dir_cascade_files + "haarcascade_frontalface_alt2.xml"
        cascade = cv2.CascadeClassifier(cascade_file)

        faces = cascade.detectMultiScale(
            image_gray,
            scaleFactor=1.1,
            minNeighbors=1,
            minSize=(48, 48),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if len(faces) >= 1:
            for (x, y, w, h) in faces:
                image_cv = cv2.rectangle(image_cv, (x, y), (x+w, y+h), (255, 0, 0), 2)

                face_image = image_gray[y:y + h, x:x + w]
                image_face_cv = cv2.resize(face_image, (48, 48))
                image_enhanced = cv2.equalizeHist(image_face_cv)
                image_chan = image_enhanced.reshape(1, 48, 48, 1)

            if time.time() - last_prediction >= 5:
                prediction = emotions[np.argmax(model.predict(image_chan), axis=1)[0]]
        else:
            prediction = "No face detected"

        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(prediction, font, 1, 2)[0]
        text_X = (image_cv.shape[1] - text_size[0]) / 2
        text_Y = (image_cv.shape[0] + text_size[1]) / 2
        cv2.putText(image_cv, prediction, (int(text_X), int(text_Y)), font, 1, (0, 255, 0), 2)

        _, jpeg = cv2.imencode('.jpg', image_cv)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    camera.release()
    cv2.destroyAllWindows()


@gzip.gzip_page
def webcam_feed(request):
    try:
        cam = cv2.VideoCapture(0)
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as ex:
        print(ex)


def webcam(request):
    if request.user.is_authenticated :
        return render(request, "web_ai/webcam.html")
    else:
        raise PermissionDenied


def homepage(request):
    return render(request, "web_ai/index.html")

