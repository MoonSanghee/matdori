from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "nickname",
            "email",
            "password1",
            "password2",
            "profile_image",
        )
        labels = {
            "username": "아이디",
            "nickname": "닉네임",
            "email": "이메일",
            "password1": "비밀번호",
            "password2": "비밀번호 확인",
            "profile_image": "프로필 이미지",
        }


class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = (
            "nickname",
            "email",
            "profile_image",
        )
        labels = {
            "nickname": "닉네임",
            "email": "이메일",
            "profile_image": "프로필 이미지",
        }
        widgets = {}
