from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()


class RegistrationPasswordValidationTests(APITestCase):
    def setUp(self):
        cache.clear()  # throttle counters are keyed by IP and persist across tests otherwise

    def test_common_password_is_rejected(self):
        response = self.client.post(
            "/api/auth/register/",
            {"username": "someuser", "email": "a@example.com", "password": "password"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="someuser").exists())

    def test_password_similar_to_username_is_rejected(self):
        response = self.client.post(
            "/api/auth/register/",
            {"username": "johnsmith", "email": "b@example.com", "password": "johnsmith123"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_strong_password_is_accepted(self):
        response = self.client.post(
            "/api/auth/register/",
            {"username": "gooduser", "email": "c@example.com", "password": "Xk9#mQ2vLp7z"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="gooduser").exists())


class TokenLifecycleTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username="tokentest", password="Xk9#mQ2vLp7z")

    def test_rotated_refresh_token_cannot_be_reused(self):
        login = self.client.post("/api/auth/login/", {"username": "tokentest", "password": "Xk9#mQ2vLp7z"})
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        old_refresh = login.data["refresh"]

        rotate = self.client.post("/api/auth/refresh/", {"refresh": old_refresh})
        self.assertEqual(rotate.status_code, status.HTTP_200_OK)

        reuse = self.client.post("/api/auth/refresh/", {"refresh": old_refresh})
        self.assertEqual(reuse.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_blacklists_current_refresh_token(self):
        login = self.client.post("/api/auth/login/", {"username": "tokentest", "password": "Xk9#mQ2vLp7z"})
        access, refresh = login.data["access"], login.data["refresh"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        logout = self.client.post("/api/auth/logout/", {"refresh": refresh})
        self.assertEqual(logout.status_code, status.HTTP_205_RESET_CONTENT)

        after_logout = self.client.post("/api/auth/refresh/", {"refresh": refresh})
        self.assertEqual(after_logout.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_works_without_an_access_token(self):
        # Regression test: logout must not require a currently-valid access token. The access
        # token expires after 30 minutes while the refresh token lasts 7 days, so a user who's
        # been idle (or whose frontend already cleared the access token before this request
        # goes out) must still be able to revoke their refresh token.
        login = self.client.post("/api/auth/login/", {"username": "tokentest", "password": "Xk9#mQ2vLp7z"})
        refresh = login.data["refresh"]

        self.client.credentials()  # no Authorization header
        logout = self.client.post("/api/auth/logout/", {"refresh": refresh})
        self.assertEqual(logout.status_code, status.HTTP_205_RESET_CONTENT)


class AuthRateLimitTests(APITestCase):
    """DEFAULT_THROTTLE_RATES: login=5/minute, register=10/minute (see settings.py)."""

    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username="ratelimittest", password="Xk9#mQ2vLp7z")

    def test_successful_login_is_not_throttled(self):
        response = self.client.post("/api/auth/login/", {"username": "ratelimittest", "password": "Xk9#mQ2vLp7z"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_wrong_password_returns_401_while_under_the_limit(self):
        # A couple of mistyped-password attempts is normal user behavior, not an attack —
        # these must still resolve as auth failures, not get swallowed by the throttle.
        for _ in range(3):
            response = self.client.post("/api/auth/login/", {"username": "ratelimittest", "password": "wrong"})
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_is_throttled_after_repeated_attempts(self):
        # 5/minute allowed — the 6th request within the window must be rejected, regardless
        # of whether the credentials on that request are even valid.
        for i in range(5):
            response = self.client.post("/api/auth/login/", {"username": "ratelimittest", "password": "wrong"})
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, f"attempt {i + 1} should not be throttled yet")

        blocked = self.client.post("/api/auth/login/", {"username": "ratelimittest", "password": "Xk9#mQ2vLp7z"})
        self.assertEqual(blocked.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_register_is_throttled_after_repeated_attempts(self):
        # 10/minute allowed — the 11th request within the window must be rejected.
        for i in range(10):
            response = self.client.post(
                "/api/auth/register/",
                {"username": f"spam_user_{i}", "email": f"spam{i}@example.com", "password": "Xk9#mQ2vLp7z"},
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, f"attempt {i + 1} should not be throttled yet")

        blocked = self.client.post(
            "/api/auth/register/",
            {"username": "spam_user_overflow", "email": "overflow@example.com", "password": "Xk9#mQ2vLp7z"},
        )
        self.assertEqual(blocked.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_login_and_register_throttles_are_independent(self):
        # Exhausting the register limit must not affect the (separate) login scope.
        for i in range(10):
            self.client.post(
                "/api/auth/register/",
                {"username": f"other_spam_{i}", "email": f"other_spam{i}@example.com", "password": "Xk9#mQ2vLp7z"},
            )
        login = self.client.post("/api/auth/login/", {"username": "ratelimittest", "password": "Xk9#mQ2vLp7z"})
        self.assertEqual(login.status_code, status.HTTP_200_OK)
