import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Project(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.id} {self.owner}"

    def save(self, *args, **kwargs):
        # TODO : make request to mongo to create record
        print(self.title)
        super().save(*args, **kwargs)
