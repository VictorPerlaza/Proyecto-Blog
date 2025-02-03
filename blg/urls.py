from django.urls import path
from . import views 
from .views import PostDetailView

urlpatterns = [
    path('', views.index, name='index'),  # Página principal del blog
    path('register', views.register, name='register'), 
    path('login', views.login, name='login'),  
    path('logout', views.cerrar, name='logout'),  
    path('profile', views.profile, name='profile'),  
    path('exp_posts', views.exp_posts, name='ex_posts'),  
    path('create_post', views.create_post, name='create_post'),  
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'), 
    path('notifications', views.notifications, name='notifications'),  
    path('user/<int:user_id>/', views.profile_detail_users, name='profile_detail_user'),
    path('search/', views.search, name='search'),
    path('post/<int:post_id>/react/<str:reaction_type>/', views.react_to_post, name='react_to_post'),
    
]


