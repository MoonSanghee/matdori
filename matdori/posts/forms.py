from django import forms
from .models import Post, Review


REVIEW_CHR_CHOICE = [
    ("라멘 맛집", "라멘 맛집"),
    ("버거 맛집", "버거 맛집"),
    ("피자 맛집", "피자 맛집"),
    ("스테이크 맛집", "스테이크 맛집"),
    ("뷰 맛집", "뷰 맛집"),
    ("칵테일 맛집", "칵테일 맛집"),
    ("국밥 맛집", "국밥 맛집"),
    ("연어 맛집", "연어 맛집"),
    ("케이크 맛집", "케이크 맛집"),
    ("곱창 맛집", "곱창 맛집"),
    ("타코 맛집", "타코 맛집"),
    ("비빔밥 맛집", "비빔밥 맛집"),
    ("장어 맛집", "장어 맛집"),
    ("소고기 맛집", "소고기 맛집"),
    ("일식 맛집", "일식 맛집"),
    ("치킨 맛집", "치킨 맛집"),
    ("훠궈 맛집", "훠궈 맛집"),
]

REVIEW_POINT_CHOICE = (
    (1, "★"),
    (2, "★★"),
    (3, "★★★"),
    (4, "★★★★"),
    (5, "★★★★★"),
)


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
            "characteristic": "태그",
            "image": "이미지",
            "thumbnail": "썸네일",
        }
        widgets = {
            "characteristic": forms.CheckboxSelectMultiple(choices=REVIEW_CHR_CHOICE)
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["content", "grade", "image"]
        labels = {
            "content": "리뷰내용",
            "grade": "맛점수",
            "sectors": "이미지",
        }

        widgets = {
            "grade": forms.Select(choices=REVIEW_POINT_CHOICE),
        }
