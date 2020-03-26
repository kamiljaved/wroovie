from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.contrib import messages


@receiver(post_save, sender=User)
def CreateProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def SaveProfile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.add_message(request, messages.WARNING, 'You are now Logged Out')


@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    messages.add_message(request, messages.SUCCESS, 'Successfully Logged In')
