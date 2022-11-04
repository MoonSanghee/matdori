from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>', views.detail, name='detail'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/likes/', views.likes, name='likes'),
    path('<int:pk>/reviews/', views.review_create, name='review_create'),
    path('<int:review_pk>/delete', views.review_delete, name='review_delete'),
    path('search/', views.search, name='search'),
]