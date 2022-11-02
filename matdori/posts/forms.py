from django import forms
from .models import Post, Review


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "address",
            "sectors",
            "phonenumber",
            "characteristic",
            "image",
            "thumbnail",
        ]
        labels = {
            "title": "상호명",
            "address": "주소",
            "sectors": "음식 종류",
            "phonenumber": "전화번호",
            "characteristic": "특징",
            "image": "이미지",
            "thumbnail": "썸네일",
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["content", "glade", "image"]
