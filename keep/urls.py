from django.urls import path

from . import views

urlpatterns = [
    # API Routes
    path("notes/<int:note_id>", views.note, name="note"),
    path("notes", views.notes, name="notes"),
    path("labels", views.labels, name="labels"),
    path("labels/<int:label_id>", views.label, name="label"),
]
