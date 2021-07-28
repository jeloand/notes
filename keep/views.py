import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import HttpResponse, render, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Label, Note

def index(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "keep/notes.html")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
@login_required
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
@login_required
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
@login_required
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
@login_required
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


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "keep/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "keep/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "keep/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "keep/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "keep/register.html")
