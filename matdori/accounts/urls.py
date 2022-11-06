from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("update/", views.update, name="update"),
    path("detail/<int:pk>", views.detail, name="detail"),
    path("logout/", views.logout, name="logout"),
    path("follow/<int:pk>/", views.follow, name="follow"),
    path("following/<int:pk>/", views.following, name="following"),
    path("follower/<int:pk>/", views.follower, name="follower"),
    path("password/", views.change_password, name="change_password"),
    path("delete/", views.delete, name="delete"),
    
]
