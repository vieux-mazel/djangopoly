from django.contrib import admin

# Register your models here.

from .models import (
    Room, Message, Spy_code
)

admin.site.register(Message)
admin.site.register(Spy_code)
admin.site.register(Room)
