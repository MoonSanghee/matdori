from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PostForm, ReviewForm
from .models import Post, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model


# Create your views here.

def index(request):
    return render(request, 'posts/index.html')

@login_required
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:index')
    else:
        post_form = PostForm()
    context = {
        'post_form': post_form
    }
    return render(request, 'posts/form.html', context)

@login_required
def update(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user == post.user:
        if request.method == 'POST':
            post_form = PostForm(request.POST, request.FILES, instance=post)
            if post_form.is_valid():
                post_form.save()
                return redirect('posts:detail', post.pk)
        else:
            post_form = PostForm(instance=post)
        context = {
            'post_form':post_form
        }
        return render(request, 'posts/form.html', context)
    else:
        messages.warning(request, '작성자만 수정할 수 있습니다.')
        return redirect('reviews:detail', post.pk)

def detail(request, pk):
    post = Post.objects.get(pk=pk)
    reviewsform = ReviewForm()
    context = {
        'post':post,
        'reviews':post.review_set.all(),
        'reviewsform':reviewsform
    }
    return render(request, 'posts/detail.html', context)

def likes(request, posts_pk):
    post = get_object_or_404(Post, pk=posts_pk)
    if request.user in post.like_user.all():
        post.like_user.remove(request.user)
        is_liked = False
    else:
        post.like_user.add(request.user)
        is_liked = True
    context = {'isLiked': is_liked, 'likeCount': post.like_user.count()}
    return JsonResponse(context)

@login_required
def review_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    reviewform = ReviewForm(request.POST, request.FILES)
    if reviewform.isvalid():
        review = reviewform.save(commit=False)
        review.post = post
        review.user = request.user
        review.save()
    context = {
        'content': review.content,
        'username': review.user.username,
        'review_image':review.image
    }
    return JsonResponse(context)