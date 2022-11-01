from django.shortcuts import redirect, render
from matdori.posts.forms import PostForm

# Create your views here.

def index(request):
    return render(request, '')

def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('')
