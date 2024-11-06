# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Notification

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        recipient = post.author.user  # Usuario autor del post
        sender = instance.author.user  # Usuario que comenta

        if recipient != sender:
            message = f"{sender.username} ha comentado en tu publicación '{post.title}'."
            Notification.objects.create(
                recipient=recipient,
                sender=sender,
                post=post,
                notification_type='comment',
                message=message
            )


