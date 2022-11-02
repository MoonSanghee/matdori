from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm


def login(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                auth_login(request, form.get_user())
                return redirect("posts:index")
        else:
            form = AuthenticationForm()
        context = {
            "form": form,
        }
        return render(request, "accounts/login.html", context)
    else:
        return redirect("accounts:index")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # 자동 로그인
            return redirect("posts:index")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "accounts/signup.html", context)


@login_required
def update(request):
    # 유효성 검사
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:detail", request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)


def detail(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    context = {
        "user": user,
    }
    return render(request, "accounts/detail.html", context)


def logout(request):
    auth_logout(request)
    messages.warning(request, "로그아웃 하였습니다.")
    return redirect("posts:index")


@login_required
def follow(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    # 스스로를 팔로우하려는 경우
    if request.user == user:
        messages.warning(request, "스스로 팔로우 할 수 없습니다.")
        return redirect("accounts:detail", pk)
    # 팔로우하고 있는 상태인 경우
    if request.user in user.folloewers.all():
        user.followers.remove(request.user)
    # 팔로우하고 있지 않았을때
    else:
        user.followers.add(request.user)
    return redirect("accounts:detail", pk)


@login_required
# 내가 팔로잉하고 있는 사람들 목록
def following(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    users = user.followings.order_by("-pk")
    context = {
        "user": user,  # 해당유저
        "users": users,  # 해당 유저가 follow하고 있는 사람들
    }
    return render(request, "accounts/following.html", context)


@login_required
# 나를 팔로잉하고 있는 사람들 목록
def follower(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    users = user.followers.order_by("-pk")
    context = {
        "user": user,  # 해당유저
        "users": users,  # 해당유저를 follow하고 있는 사람들
    }
    return render(request, "accounts/follower.html", context)

# 비밀번호 변경
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "비밀번호를 변경했습니다.")
            return redirect("accounts:index")
        else:
            messages.error(request, "비밀번호 변경에 실패했습니다.")
    else:
        form = PasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/change_password.html", context)

# 회원탈퇴
@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect("posts:index")
