from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# here is model for profile amjad.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # birth_date = models.DateField(blank=False)
    bio = models.TextField(blank=True)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
    