from django.shortcuts import render, redirect
from django.views.decorators import gzip
from django.http import StreamingHttpResponse, JsonResponse
import numpy as np
import cv2
import threading
import base64


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        dir_cascade_files = r"/home/greywater/Documents/Kirae/app/src/model/.opencv/haarcascades/"
        cascade_file = dir_cascade_files + "haarcascade_frontalface_alt2.xml"

        cascade = cv2.CascadeClassifier(cascade_file)

        faces = cascade.detectMultiScale(
            gray_image,
            scaleFactor=1.1,
            minNeighbors=1,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if len(faces) == 1:
            for (x, y, w, h) in faces:
                fc = gray_image[y:y+h, x:x+w]
                roi = cv2.resize(fc, (64, 64))
                pred = np.argmax(model.predict(roi[np.newaxis, :, :, np.newaxis]), axis=1)[0]

                cv2.putText(image, emotions[pred], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def webcam_feed(request):
    #print(request.path)
    #try:
    #    cam = VideoCamera()
    #    return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    #except Exception as ex:
    #    print(ex)
    if request.method == 'POST':
        try:
            frame_ = request.POST.get('image')
            frame_ = str(frame_)
            data = frame_.replace('data:image/jpeg;base64,', '')
            data = data.replace(' ', '+')
            imgdata = base64.b64decode(data)
            print(imgdata)
            filename = 'some_image.jpg'
            with open(filename, 'wb') as f:
                f.write(imgdata)
        except:
            print('Error')

        return JsonResponse({'Json': data})


def webcam(request):
    return render(request, "web_ai/webcam.html")


def homepage(request):
    return render(request, "web_ai/index.html")

