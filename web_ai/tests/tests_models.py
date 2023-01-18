from django.test import TestCase
from accounts.models import AppUser, History
from django.contrib.auth import authenticate


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




#history_test = History.objects.create(name="test_file.png", file_path="file/test_file.png", prediction="", true_prediction="", user=user_test)
