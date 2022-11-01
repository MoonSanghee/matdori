from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "accounts"

urlpatterns = [
    path("", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("update/", views.update, name="update"),
    path("detail/<int:pk>", views.detail, name="detail"),
    path("logout/", views.logout, name="logout"),
    path("<int:pk>/follow/", views.follow, name="follow"),
]
