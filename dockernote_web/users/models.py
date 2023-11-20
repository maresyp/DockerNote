from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Mężczyzna'),
        ('K', 'Kobieta'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    city = models.CharField(max_length=50, null=True, blank=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18), MaxValueValidator(125)], null=True, blank=True)
    bio = models.TextField(max_length=1000, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profiles', null=True, blank=True, default='profiles/user-default.png')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')

    def __str__(self) -> str:
        return str(self.user)

    @property
    def imageURL(self):
        """
        Returns the URL of the user's profile image.

        Returns:
        str: The URL of the profile image
        """
        try:
            url = self.profile_image.url
        except Exception:
            url = ''
        return url
