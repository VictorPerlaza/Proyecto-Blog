from django.urls import path
from . import views 
from .views import PostDetailView

urlpatterns = [
    path('', views.index, name='index'),  # Página principal del blog
    path('register', views.register, name='register'), 
    path('login', views.login, name='login'),  
    path('logout', views.cerrar, name='logout'),  
    path('profile', views.profile, name='profile'),  
    path('create_post', views.create_post, name='create_post'),  
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'), 
]