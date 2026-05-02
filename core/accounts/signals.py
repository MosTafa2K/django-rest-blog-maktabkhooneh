from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, Profile


@receiver(post_save, sender=User)
def create_user_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.db_manager(instance._state.db).create(user=instance)
        print(f"Profile {instance} has been created!")
