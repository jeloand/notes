import json
from django.shortcuts import HttpResponse, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Label, Note

@csrf_exempt
def notes(request):
    if request.method == "POST":
        data = json.loads(request.body)
        note = Note(
            # user = request.user,
            title = data.get("title", ""),
            body = data.get("body", ""),
            color = data.get("color", "000000")
        )
        note.save()

        if data.get("labels") is not None:
            labels = []
            for label_id in data["labels"]:
                try:
                    labels += [Label.objects.get(id=label_id)]
                except Label.DoesNotExist:
                    note.delete()
                    return JsonResponse({
                        "error": f"Label {label_id} does not exist."
                    }, status=400)
            note.labels.add(*labels)

        return  JsonResponse({"message": "Note saved."}, status=201)

    elif request.method == "GET":
        return JsonResponse([note.serialize() for note in Note.objects.all()], safe=False)

    else:
        return JsonResponse({
            "error": "GET or POST request required."
        }, status=400)

@csrf_exempt
def note(request, note_id):
    try:
        # note = Note.objects.get(owner=request.user, pk=note_id)
        note = Note.objects.get(pk=note_id)
    except Note.DoesNotExist:
        return JsonResponse({"error": "Note not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(note.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("title") is not None:
            note.title = data["title"]
        if data.get("body") is not None:
            note.body = data["body"]
        if data.get("color") is not None:
            note.color = data["color"]
        if data.get("labels") is not None:
            labels = []
            for label_id in data["labels"]:
                try:
                    labels += [Label.objects.get(id=label_id)]
                except Label.DoesNotExist:
                    return JsonResponse({
                        "error": f"Label {label_id} does not exist."
                    }, status=400)
            note.labels.add(*labels)
        if data.get("archived") is not None:
            note.archived = data["archived"]
        if data.get("deleted") is not None:
            note.deleted = data["deleted"]
        if data.get("pinned") is not None:
            note.pinned = data["pinned"]
        note.save()
        return HttpResponse(status=204)

    elif request.method == "DELETE":
        note.delete()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET, PUT, or DELETE request required."
        }, status=400)

@csrf_exempt
def labels(request):
    if request.method == "GET":
        return JsonResponse([label.serialize() for label in Label.objects.all()], safe=False)

    elif request.method == "POST":
        data = json.loads(request.body)
        if data.get("name") is None:
            return JsonResponse({"error": "Label name required."}, status=400)

        if data["name"] == "":
            return JsonResponse({"error": "Label cannot be blank."}, status=400)
        elif data["name"] in [label.name for label in Label.objects.all()]:
            return JsonResponse({"error": "Label already exists."}, status=400)

        label = Label(name=data["name"])
        label.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET or POST request required."
        }, status=400)

@csrf_exempt
def label(request, label_id):
    try:
        label = Label.objects.get(pk=label_id)
    except Label.DoesNotExist:
        return JsonResponse({"error": "Label not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(label.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("new_name") is None:
            return JsonResponse({"error": "Label new_name required."}, status=400)

        if data["new_name"] == "":
            return JsonResponse({"error": "Label cannot be blank."}, status=400)
        elif data["new_name"] in [label.name for label in Label.objects.all()]:
            return JsonResponse({"error": "Label already exists."}, status=400)

        label.name = data["new_name"]
        label.save()
        return HttpResponse(status=204)

    elif request.method == "DELETE":
        label.delete()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET, PUT, or DELETE request required."
        }, status=400)
