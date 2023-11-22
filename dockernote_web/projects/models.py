import uuid

import requests
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Project(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=5000, blank=True, default="")
    creation_date = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.owner} {self.title}"

    def save(self, *args, **kwargs):
        # TODO : make request to mongo to create record
        super().save(*args, **kwargs)
