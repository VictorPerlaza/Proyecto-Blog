from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página principal del blog
    path('register', views.register, name='register'), 
    path('login', views.login, name='login'),  
    path('logout', views.cerrar, name='logout'),  
    path('profile', views.profile, name='profile'),  
    path('create_post', views.create_post, name='create_post'),  
    path('post/<int:id>/', views.post_detail, name='post_detail'),  # Detalle de un post
] 