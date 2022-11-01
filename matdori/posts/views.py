from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PostForm, ReviewForm
from .models import Post, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q



# Create your views here.

def index(request):
    posts = Post.objects.order_by('-pk')
    context = {
        'posts':posts
    }
    return render(request, 'posts/index.html', context)

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

@login_required
def delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user == post.user:
        post.delete()
        return redirect('posts:index')
    else:
        messages.warning(request, '작성자만 삭제할 수 있습니다.')
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

@login_required
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
    if reviewform.is_valid():
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

@login_required
def review_delete(request, post_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if review.user == request.user:
        review.delete()
        return redirect('posts:detail', post_pk)
    messages.warning(request, '작성자만 삭제할 수 있습니다.')
    return redirect('posts:detail', post_pk)

def search(requset):
    searched = requset.GET.get('searched', False)
    field = requset.GET.get('field')
    if field == '1':
        posts = Post.objects.filter(Q(title__contains=searched) | Q(address__contains=searched) | Q(sectors__username__contains=searched) | Q(characteristic__username__contains=searched)).order_by('-pk')
    elif field == '2':
        posts = Post.objects.filter(Q(title__contains=searched)).order_by('-pk')
    elif field == '3':
        posts = Post.objects.filter(Q(adress__contains=searched)).order_by('-pk')
    elif field == '4':
        posts = Post.objects.filter(Q(sectors__contains=searched)).order_by('-pk')
    elif field == '5':
        posts = Post.objects.filter(Q(characteristic__contains=searched)).order_by('-pk')
    if not searched:
        posts = []
        text = '검색어를 입력해 주세요.'
    elif not len(posts):
        text = '검색 결과가 없습니다.'
    else:
        text = ''
    context = {
        'posts':posts,
        'text':text,
        'searched':searched,
        'field':field
    }
    return render(requset, 'posts/search/', context)