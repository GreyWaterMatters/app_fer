import cv2
import os

from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm

from datetime import datetime

from .forms import NewUserForm
from .functions import preprocess_image
from .models import History
from web_ai.logging import logger


# Create your views here.
def register_request(request):
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            logger.info(f'New user registered: {user}')
            return redirect("homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
        logger.error('Failed registration')
    form = NewUserForm()

    return render(request=request, template_name="accounts/register.html", context={"register_form": form})


def login_request(request):
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                logger.info(f'User {username} is logged !')
                return redirect("homepage")
            else:
                logger.error(f'Failed login')
                messages.error(request, "Invalid username or password.")
        else:
            logger.error(f'Failed login')
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="accounts/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("homepage")


def profile(request):
    if request.user.is_authenticated:
        predictions = History.objects.all().filter(user_id=request.user.id)
        if len(predictions) >= 1:
            return render(request, "accounts/profile.html", {"predictions": predictions})
        return render(request, "accounts/profile.html")
    else:
        raise PermissionDenied


def predict_emotion(request):
    print(request)
    if request.method == 'POST':

        today = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
        path = settings.MEDIA_ROOT

        image_obj = request.FILES['face-image']
        image_read = request.FILES['face-image'].read()
        result = preprocess_image(image_read)

        if len(result) == 2:

            if request.user.is_authenticated:

                user_instance = request.user
                os.makedirs(os.path.join(path, f'file/{str(user_instance.id)}'), exist_ok=True)

                file_path = f'file/{user_instance.id}/prediction_{today}.png'

            else:
                file_path = f'temp/prediction_anonymous.png'

            cv2.imwrite(os.path.join(path, file_path), result[1])

            return render(request, "web_ai/index.html", {"prediction": result[0], "image": file_path,
                                                         "image_name": image_obj.name})
        else:
            return render(request, "web_ai/index.html", {"prediction": result})


def check_prediction(request):

    if request.method == "POST":
        user_instance = request.user
        image_name = request.POST["file_name"]
        file_path = request.POST["file_path"]
        prediction = request.POST["prediction"]
        true_prediction = request.POST["true_prediction"]

        image_file = History.objects.create(
            name=image_name,
            file_path=file_path,
            prediction=prediction,
            true_prediction=true_prediction,
            user=user_instance
        )

    return redirect("homepage")
