from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "phone", "company_name"]
        read_only_fields = ["id", "role"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name", "phone", "company_name"]

    def validate(self, attrs):
        # Runs the project's full AUTH_PASSWORD_VALIDATORS (similarity, common-password,
        # numeric-only) against the password, not just the min_length check above.
        temp_user = User(
            username=attrs.get("username", ""),
            email=attrs.get("email", ""),
            first_name=attrs.get("first_name", ""),
            last_name=attrs.get("last_name", ""),
        )
        validate_password(attrs["password"], user=temp_user)
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data, role=User.Role.CLIENT)
        user.set_password(password)
        user.save()
        return user
