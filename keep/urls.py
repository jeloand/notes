from django.urls import path

from . import views

urlpatterns = [
    # API Routes
    path("notes/add", views.add, name="add"),
    path("notes/<int:note_id>", views.note, name="note"),
    path("notes", views.notes, name="notes"),
]
