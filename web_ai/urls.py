"""web_ai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from web_ai.views import homepage, webcam, webcam_feed
from accounts.views import register_request, login_request, logout_request, profile, predict_emotion, check_prediction

urlpatterns = [
                  path("", homepage, name="homepage"),
                  path("webcam/", webcam, name="webcam"),
                  path("webcam_feed", webcam_feed, name="webcam_feed"),
                  path("submit_image/", predict_emotion, name="predict_image"),
                  path("check_prediction/", check_prediction, name="check_prediction"),
                  path("register/", register_request, name="register"),
                  path("login/", login_request, name="login"),
                  path("logout/", logout_request, name="logout"),
                  path("profile/", profile, name="profile"),
                  path('admin/', admin.site.urls),
                  path('', include('django_prometheus.urls'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
