from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import StreamingHttpResponse

from django.views.decorators import gzip
import cv2

from accounts.functions import preprocess_image


def gen(camera):
    while True:
        ret, img = camera.read()
        img_bytes = cv2.imencode('.jpg', img)[1].tobytes()
        result = preprocess_image(img_bytes)

        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(result[0], font, 1, 2)[0]
        text_X = (result[1].shape[1] - text_size[0]) / 2
        text_Y = (result[1].shape[0] + text_size[1]) / 2
        cv2.putText(result[1], result[0], (int(text_X), int(text_Y)), font, 1, (0, 255, 0), 2)

        _, jpeg = cv2.imencode('.jpg', result[1])

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

