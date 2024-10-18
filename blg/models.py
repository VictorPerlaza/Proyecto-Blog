from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        # Redimensionar la imagen del avatar
        if self.avatar:
            img = Image.open(self.avatar.path)

            # Especificamos las dimensiones deseadas
            output_size = (300, 300)

            # Redimensionamos la imagen si es más grande que las dimensiones deseadas
            if img.height > output_size[0] or img.width > output_size[1]:
                img = img.resize(output_size, Image.Resampling.LANCZOS)  
                img.save(self.avatar.path)  # Guardamos la imagen redimensionada

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


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

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        # Redimensionar la imagen del avatar
        if self.image:
            img = Image.open(self.image.path)

            # Especificamos las dimensiones deseadas
            output_size = (800, 400)

            # Redimensionamos la imagen si es más grande que las dimensiones deseadas
            if img.height > output_size[0] or img.width > output_size[1]:
                img = img.resize(output_size, Image.Resampling.LANCZOS)  
                img.save(self.image.path)  # Guardamos la imagen redimensionada




class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Cambiado a ForeignKey
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    def __str__(self):
        return f'Comentario de {self.author.user.username} en {self.post.title}'
