from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class UserRegistrationTest(APITestCase):
    def test_create_account(self):
        url = reverse('api_users')
        data = {
            "id": 99,
            "password": "pbkdf2_sha256$320000$y",
            "last_login": "2022-05-04T20:54:58.681660Z",
            "is_superuser": True,
            "username": "super_django_tester",
            "first_name": "Cheyenne",
            "last_name": "Bees",
            "email": "",
            "is_staff": False,
            "is_active": True,
            "date_joined": "2022-05-01T18:46:30.510028Z",
            "groups": [],
            "user_permissions": [1,2,3]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'superdjangotester')
        self.assertEqual(User.objects.get().first_name, 'Cheyenne')