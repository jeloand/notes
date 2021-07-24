from django.contrib import admin

# Register your models here.
from keep.models import User, Label, Note

admin.site.register(User)
admin.site.register(Label)
admin.site.register(Note)
