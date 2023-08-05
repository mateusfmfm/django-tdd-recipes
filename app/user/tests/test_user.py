from django.contrib.auth import get_user_model
from django.test import testcases
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")
USER_PAYLOAD = {
    "email": "test@example.com",
    "password": "testpass123",
    "name": "Test name",
}
USER_PAYLOAD_PASS_SHORT = {
    "email": "test@example.com",
    "password": "pw",
    "name": "Test name",
}


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(testcases):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = USER_PAYLOAD
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        payload = USER_PAYLOAD
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        payload = USER_PAYLOAD_PASS_SHORT
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"])\
            .exists()
        self.assertFalse(user_exists)
