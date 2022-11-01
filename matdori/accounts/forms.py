from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "nickname",
            "password1",
            "password2",
            "image",
        )
        labels = {
            "username": "id",
            "nickname": "닉네임",
            "password1": "비밀번호",
            "password2": "비밀번호 확인",
            "image": "프로필 이미지",
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "nickname",
            "email",
            "image",
        )
        labels = {
            "nickname": "닉네임",
            "email": "이메일",
            "image": "프로필 이미지",
        }
