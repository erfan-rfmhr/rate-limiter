from rest_framework.reverse import reverse
from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models.users import User
from unittest.mock import patch
from rest_framework.throttling import UserRateThrottle
import time


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "test_cache",
        }
    }
)
class WalletThrottlingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username="user1", password="testpass123")
        self.user2 = User.objects.create_user(username="user2", password="testpass123")
        self.deposit_url = reverse("wallets-deposit")
        self.withdraw_url = reverse("wallets-withdraw")
        self.data = {"balance": 100}
        UserRateThrottle.cache.clear()

    def test_user_can_make_5_requests_without_throttling(self):
        self.client.force_authenticate(user=self.user1)

        for i in range(5):
            response = self.client.post(self.deposit_url, self.data, format="json")
            self.assertNotEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        response = self.client.post(self.withdraw_url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_6th_request_is_throttled(self):
        self.client.force_authenticate(user=self.user1)

        for i in range(5):
            self.client.post(self.deposit_url, self.data, format="json")

        response = self.client.post(self.deposit_url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    @patch.object(UserRateThrottle, "timer")
    def test_user_can_request_after_60_seconds(self, mock_timer):
        self.client.force_authenticate(user=self.user1)

        initial_time = time.time()
        mock_timer.return_value = initial_time

        for i in range(5):
            self.client.post(self.deposit_url, self.data, format="json")

        response = self.client.post(self.deposit_url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        mock_timer.return_value = initial_time + 61

        response = self.client.post(self.deposit_url, self.data, format="json")
        self.assertNotEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_throttling_is_user_specific(self):
        self.client.force_authenticate(user=self.user1)

        for i in range(5):
            self.client.post(self.deposit_url, self.data, format="json")

        response = self.client.post(self.deposit_url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        self.client.force_authenticate(user=self.user2)

        for i in range(5):
            response = self.client.post(self.deposit_url, self.data, format="json")
            self.assertNotEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        response = self.client.post(self.deposit_url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
