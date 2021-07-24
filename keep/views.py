import json
from django.shortcuts import HttpResponse, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Label, Note

@csrf_exempt
def add(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    note = Note(
        # owner = request.user,
        title = data.get("title", ""),
        body = data.get("body", ""),
        color = data.get("color", "000000"),
        # label = data.get("label")
    )
    note.save()

    return  JsonResponse({"message": "Note saved."}, status=201)

@csrf_exempt
def note(request, note_id):
    try:
        # note = Note.objects.get(owner=request.user, pk=note_id)
        note = Note.objects.get(pk=note_id)
    except Note.DoesNotExist:
        return JsonResponse({"error": "Note not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(note.serialize())

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("title") is not None:
            note.title = data["title"]
        if data.get("body") is not None:
            note.body = data["body"]
        if data.get("color") is not None:
            note.color = data["color"]
        if data.get("label_id") is not None:
            try:
                label = Label.objects.get(id=label_id)
                note.label = label_id
            except Label.DoesNotExist:
                return JsonResponse({
                    "error": f"Label {label_id} does not exist."
                }, status=400)
        if data.get("archived") is not None:
            note.archived = data["archived"]
        if data.get("deleted") is not None:
            note.deleted = data["deleted"]
        if data.get("pinned") is not None:
            note.pinned = data["pinned"]
        note.save()
        return HttpResponse(status=204)

    if request.method == "DELETE":
        note.delete()
        return HttpResponse(status=204)

def notes(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    notes = Note.objects.all()
    return JsonResponse([note.serialize() for note in notes], safe=False)