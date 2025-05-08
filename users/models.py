from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='static/avatars/', default='static/avatars/default.png')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
