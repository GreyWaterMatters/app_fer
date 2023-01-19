from django.test import TestCase
from accounts.models import AppUser, History
from django.contrib.auth import authenticate
from accounts.functions import preprocess_image
import cv2


# Create your tests here.
class UserTest(TestCase):

    def setUp(self):
        self.user = AppUser.objects.create_user(username="unit_test", email="unit_test@test.com",
                                                password="p@sSword123")
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct_login(self):
        user = authenticate(email="unit_test@test.com", password="p@sSword123")
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(email="unit_test@test.com", password="12345")
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_wrong_email(self):
        user = authenticate(email="unit_test@test.co", password="p@sSword123")
        self.assertFalse((user is not None) and user.is_authenticated)


class HistoryTest(TestCase):

    def setUp(self):
        self.user = AppUser.objects.create_user(username="unit_test", email="unit_test@test.com",
                                                password="p@sSword123")
        self.user.save()

        image = cv2.imread("/home/greywater/Documents/Kirae/app/image_test/2022-11-29_18-11.png", cv2.IMREAD_UNCHANGED)
        image_bytes = cv2.imencode('.png', image)[1].tobytes()
        self.prediction = preprocess_image(image_bytes)
        self.history = History(name="test_file.png", file_path="file/test_file.png", prediction=self.prediction[0],
                               true_prediction="Angry", user=self.user)

        self.history.save()

    def tearDown(self):
        self.history.delete()
        self.user.delete()

    def test_history_creation(self):
        history_test = History.objects.get(id=self.history.id)
        self.assertEqual(history_test.true_prediction, "Angry")
        self.assertEqual(history_test.prediction, self.prediction[0])

