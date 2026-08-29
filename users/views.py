from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    # Dedicated, stricter rate limit (see DEFAULT_THROTTLE_RATES["register"]) — prevents
    # automated mass account creation without affecting normal signup.
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "register"


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class LoginView(TokenObtainPairView):
    """POST {username, password} -> {access, refresh}"""
    permission_classes = [permissions.AllowAny]
    # Dedicated, stricter rate limit (see DEFAULT_THROTTLE_RATES["login"]) — the shared
    # 30/minute anon rate is too generous to meaningfully slow down credential stuffing or
    # brute-force attempts against a specific account.
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"


class LogoutView(APIView):
    """POST {refresh} -> blacklists the refresh token server-side so it can't be reused after logout.

    Deliberately AllowAny rather than IsAuthenticated: the refresh token itself is the
    credential being revoked, and it's valid for 7 days while the access token expires after
    30 minutes — requiring a still-valid access token would make logout fail for anyone whose
    access token had already expired, which defeats the point of letting them log out."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"detail": "refresh is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            RefreshToken(refresh).blacklist()
        except TokenError:
            return Response({"detail": "Invalid or already-blacklisted token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_205_RESET_CONTENT)
