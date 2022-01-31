from django.shortcuts import render

# Create your views here.
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Notification

@receiver(post_save, sender=Comment)
def auto_create_notification(sender, instance, created, **kwargs):
    if created:
        # instance holds the new comment (reply), but you also have to fetch
        # original comment and the user who created it
        parent_comment = instance.parent_comment
        parent_user = parent_comment.user            
        Notification.objects.create(user=parent_user,
                                    type="reply_created")