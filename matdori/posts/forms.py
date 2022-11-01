from django import forms
from .models import Post, Review

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'address', 'sectors', 'phonenumber', 'glade', 'characteristic', 'image', 'thumbnail', 'like_user']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'image']