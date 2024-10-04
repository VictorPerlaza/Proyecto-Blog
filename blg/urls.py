from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página principal del blog
    path('register', views.register, name='register'), 
    path('login', views.login, name='login'),  
    path('logout', views.cerrar, name='logout'),  
    path('post/<int:id>/', views.post_detail, name='post_detail'),  # Detalle de un post
]