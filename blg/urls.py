from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blog_index'),  # Página principal del blog
    path('post/<int:id>/', views.post_detail, name='post_detail'),  # Detalle de un post
]