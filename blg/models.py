from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Relación con el modelo User
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username  # Mostrar el nombre de usuario cuando se represente el autor

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Cambiado a ForeignKey
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    def __str__(self):
        return f'Comentario de {self.author.user.username} en {self.post.title}'
