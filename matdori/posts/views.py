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
    posts = Post.objects.order_by("-pk")
    context = {"posts": posts}
    return render(request, "posts/index.html", context)


@login_required
def create(request):
    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("posts:index")
    else:
        post_form = PostForm()
    context = {"post_form": post_form}
    return render(request, "posts/form.html", context)


@login_required
def update(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user == post.user:
        if request.method == "POST":
            post_form = PostForm(request.POST, request.FILES, instance=post)
            if post_form.is_valid():
                post_form.save()
                return redirect("posts:detail", post.pk)
        else:
            post_form = PostForm(instance=post)
        context = {"post_form": post_form}
        return render(request, "posts/form.html", context)
    else:
        messages.warning(request, "작성자만 수정할 수 있습니다.")
        return redirect("posts:detail", post.pk)


@login_required
def delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user == post.user:
        post.delete()
        return redirect("posts:index")
    else:
        messages.warning(request, "작성자만 삭제할 수 있습니다.")
        return redirect("posts:detail", pk)


def detail(request, pk):
    post = Post.objects.get(pk=pk)
    reviewsform = ReviewForm()
    reviews = post.review_set.all()
    points = 0
    for review in reviews:
        points += review.glade
    if len(reviews):
        points = round(points / len(reviews), 1)
    context = {
        "post": post,
        "reviews": post.review_set.all(),
        "reviewsform": reviewsform,
        "points": points,
    }
    return render(request, "posts/detail.html", context)


@login_required
def likes(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.like_user.all():
        post.like_user.remove(request.user)
        is_liked = False
    else:
        post.like_user.add(request.user)
        is_liked = True
    context = {"isLiked": is_liked, "likeCount": post.like_user.count()}
    return JsonResponse(context)


@login_required
def review_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post_form = ReviewForm(request.POST, request.FILES)
        if post_form.is_valid():
            review = post_form.save(commit=False)
            review.user = request.user
            review.post = Post.objects.get(pk=pk)
            review.save()
            return redirect("posts:detail", pk)
    else:
        post_form = ReviewForm()
    context = {"post_form": post_form}
    return render(request, "posts/form.html", context)


@login_required
def review_delete(request, post_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if review.user == request.user:
        review.delete()
        return redirect("posts:detail", post_pk)
    else:
        messages.warning(request, "작성자만 삭제할 수 있습니다.")
    return redirect("posts:detail", post_pk)


def search(requset):
    searched = requset.GET.get("searched", False)
    field = requset.GET.get("field")
    if field == "1":
        posts = Post.objects.filter(
            Q(title__contains=searched)
            | Q(address__contains=searched)
            | Q(sectors__contains=searched)
            | Q(characteristic__contains=searched)
        ).order_by("-pk")
    elif field == "2":
        posts = Post.objects.filter(Q(title__contains=searched)).order_by("-pk")
    elif field == "3":
        posts = Post.objects.filter(Q(adress__contains=searched)).order_by("-pk")
    elif field == "4":
        posts = Post.objects.filter(Q(sectors__contains=searched)).order_by("-pk")
    elif field == "5":
        posts = Post.objects.filter(Q(characteristic__contains=searched)).order_by(
            "-pk"
        )
    if not searched:
        posts = []
        text = "검색어를 입력해 주세요."
    elif not len(posts):
        text = "검색 결과가 없습니다."
    else:
        text = ""
    context = {"posts": posts, "text": text, "searched": searched, "field": field}
    return render(requset, "posts/search.html", context)
