from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Label(models.Model):
    # user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="notes")
    name = models.CharField(max_length=64, unique=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Note(models.Model):
    # user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    color = models.CharField(max_length=6)
    archived = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)
    labels = models.ManyToManyField("Label", related_name="notes")

    def serialize(self):
        return {
            "id": self.id,
            # "user": self.user,
            "title": self.title,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "color": self.color,
            "archived": self.archived,
            "deleted": self.deleted,
            "pinned": self.pinned,
            "labels": dict(zip(
                [label.id for label in self.labels.all()],
                [label.name for label in self.labels.all()],
            ))
        }
