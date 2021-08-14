from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile


#####~~~~~ SIGNAL ~~~~~#####
@receiver(post_save, sender=User)
def CreateProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# #####~~~~~ SIGNAL ~~~~~#####
# @receiver(post_save, sender=User)
# def SaveProfile(sender, instance, **kwargs):
#     instance.profile.save()

# #####~~~~~ SIGNAL ~~~~~#####
# @receiver(user_logged_out)
# def on_user_logged_out(sender, request, **kwargs):
#     messages.add_message(request, messages.WARNING, 'You are now Logged Out')

# #####~~~~~ SIGNAL ~~~~~#####
# @receiver(user_logged_in)
# def on_user_logged_in(sender, request, **kwargs):
#     messages.add_message(request, messages.SUCCESS, 'Successfully Logged In')
