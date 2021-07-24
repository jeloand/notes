from django.urls import path

from . import views

urlpatterns = [
    # API Routes
    path("notes/<int:note_id>", views.note, name="note"),
    path("notes", views.notes, name="notes"),
]
