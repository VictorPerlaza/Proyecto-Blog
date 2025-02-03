from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

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
    title = models.CharField(max_length=80)
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
                
    def __str__(self):
        return self.title
    
    def likes_count(self):
        return self.reactions.filter(reaction_type='like').count()

    def loves_count(self):
        return self.reactions.filter(reaction_type='love').count()

    def dislikes_count(self):
        return self.reactions.filter(reaction_type='dislike').count()

    def total_reactions(self):
        return self.reactions.count()



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Cambiado a ForeignKey
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    def __str__(self):
        return f'Comentario de {self.author.user.username} en {self.post.title}'
    

class Reaction(models.Model):
    REACTION_TYPES = (
        ('like', 'Like'),
        ('love', 'Love'),
        ('dislike', 'Dislike'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=10, choices=REACTION_TYPES)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post', 'reaction_type')  # Evita duplicados por usuario y post

    def __str__(self):
        return f"{self.user.username} reacted {self.reaction_type} to {self.post.title}"


@receiver(post_save, sender=Comment)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.post.author.user,  # Autor del post
            sender=instance.author.user,  # Autor del comentario
            post=instance.post,
            notification_type='comment',
            message=f"{instance.author.user.username} comentó en tu post '{instance.post.title}'."
        )

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('comment', 'Comment'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notification for {self.recipient.username} - {self.notification_type}"
    
