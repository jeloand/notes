from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Label(models.Model):
    name = models.CharField(max_length=64)

class Note(models.Model):
    # owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    color = models.CharField(max_length=6)
    archived = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)
    label = models.ManyToManyField("Label", related_name="notes", null=True)

    def serialize(self):
        return {
            "id": self.id,
            # "owner": self.owner,
            "title": self.title,
            "body": self.body,
            "timestamp": self.timestamp,
            "color": self.color,
            "archived": self.archived,
            "deleted": self.deleted,
            "pinned": self.pinned,
            "label": self.label
        }
