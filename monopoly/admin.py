from django.contrib import admin

# Register your models here.

from .models import (
    Game, Square, Player, Street, Utility, Effect, Special, UserProfile
)

admin.site.register(Game)
admin.site.register(Square)
admin.site.register(Player)
admin.site.register(Street)
admin.site.register(Utility)
admin.site.register(Effect)
admin.site.register(Special)
admin.site.register(UserProfile)