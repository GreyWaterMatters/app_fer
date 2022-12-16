from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView

from accounts.functions import get_image_webcam


class ImageFaceDetect(TemplateView):
    template_name = "web_ai/webcam.html"

    def post(self, request, *args, **kwargs):
        data = request.POST.get('image')
        try:
            image_data = get_image_webcam(data)
            if image_data:
                return JsonResponse(status=200, data={'image': image_data, 'message': 'Face detected'})
        except Exception as e:
            pass
        return JsonResponse(status=400, data={'errors': {'error_message': 'No face detected'}})


def homepage(request):
    return render(request, "web_ai/index.html")

