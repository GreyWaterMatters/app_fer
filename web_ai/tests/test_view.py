from django.test import TestCase
from django.urls import reverse

from accounts.models import AppUser


class ProfileTest(TestCase):

    def setUp(self):
        self.user = AppUser.objects.create_user(username="unit_test", email="unit_test@test.com",
                                                password="p@sSword123")
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_not_authenticated_profile(self):
        url = reverse("profile")
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, "accounts/profile.html")
        self.failUnlessEqual(response.status_code, 403)

    def test_authenticated_profile(self):
        self.client.login(email="unit_test@test.com", password="p@sSword123")
        url = reverse("profile")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "accounts/profile.html")
        self.failUnlessEqual(response.status_code, 200)


class WebcamTest(TestCase):

    def setUp(self):
        self.user = AppUser.objects.create_user(username="unit_test", email="unit_test@test.com",
                                                password="p@sSword123")
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_not_authenticated_webcam(self):
        url = reverse("webcam")
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, "web_ai/webcam.html")
        self.failUnlessEqual(response.status_code, 403)

    def test_authenticated_webcam(self):
        self.client.login(email="unit_test@test.com", password="p@sSword123")
        url = reverse("webcam")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "web_ai/webcam.html")
        self.failUnlessEqual(response.status_code, 200)
