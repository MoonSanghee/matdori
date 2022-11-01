from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>', views.detail, name='detail'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:reviews_pk>/likes/', views.likes, name='likes'),
    path('<int:pk>/review/', views.review_create, name='review_create'),
]