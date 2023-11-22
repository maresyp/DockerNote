from __future__ import annotations

import requests
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import Project


@receiver(post_save, sender=Project)
def create_mongodb_instance(sender, instance, created, **kwargs):
    """
    """
    if not created:
        return

    url: str = 'http://file_server:8000/add_project'
    body: dict[str, str] = {
        '_id': str(instance.id),
        'owner_id': str(instance.owner.id),
        'title': str(instance.title),
        'description': str(instance.description),
    }

    response = requests.post(url, json=body, timeout=10)
    if response.status_code != 201:
        raise Exception(f'error: {response.json()["detail"]}')