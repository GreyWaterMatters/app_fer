from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.contrib import messages
from accounts.forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm

from .functions import preprocess_image
from .models import History

from tensorflow.keras.models import load_model
from datetime import date
import numpy as np
import cv2
import os

emotions = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}


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
            return redirect("homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
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
                return redirect("homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="accounts/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("homepage")


def profile(request):
    if request.user.is_authenticated:
        return render(request, "accounts/profile.html")
    else:
        return render(request, "error.html")


def predict_emotion(request):
    if request.method == 'POST':

        today = date.today().strftime('%d-%m-%Y_%H-%M-%S')
        path = settings.MEDIA_ROOT

        image_obj = request.FILES['face-image']
        image_read = request.FILES['face-image'].read()
        image = preprocess_image(image_read)

        print(type(image_obj))

        model = load_model("/home/greywater/Documents/Kirae/app/src/model/model_feat_ex_3_contrast_detect_face")

        prediction = np.argmax(model.predict(image[0]), axis=1)[0]

        if request.user.is_authenticated:

            user_instance = request.user
            os.makedirs(os.path.join(path, f'file/{str(user_instance.id)}'), exist_ok=True)

            file_path = f'file/{user_instance.id}/prediction_{today}.png'

            image_file = History.objects.create(
                name=image_obj.name,
                file_path=os.path.join(path, file_path),
                prediction=emotions[prediction],
                user=user_instance
            )

        else:
            file_path = f'temp/prediction_{anonymous}.png'

        cv2.imwrite(os.path.join(path, file_path), image[1])

        return render(request, "web_ai/index.html", {"prediction": emotions[prediction], "image": file_path})
