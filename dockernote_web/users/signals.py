from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    """
    Signal for creating a Profile instance whenever a new User is created.

    This signal receiver listens to the post_save signal sent by User model
    and creates a new Profile instance associated with the User.

    Args:
        sender (model): The model that sends the signal.
        instance (User instance): The instance of User model that has been saved.
        created (bool): A boolean value indicating whether a new record was created.
        **kwargs: Arbitrary keyword arguments.
    """
    if created:
        user = instance
        Profile.objects.create(
            user=user,
        )


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    """
    Signal for deleting a User instance when associated Profile is deleted.

    This signal receiver listens to the post_delete signal sent by Profile model
    and deletes the associated User instance.

    Args:
        sender (model): The model that sends the signal.
        instance (Profile instance): The instance of Profile model that has been deleted.
        **kwargs: Arbitrary keyword arguments.
    """
    try:
        instance.user.delete()
    except Exception as e:
        print(f'{e} raised during deleting user')
