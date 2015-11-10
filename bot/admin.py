from django.contrib import admin

from .models import Command, Bot, Storage


admin.site.register(Command)
admin.site.register(Bot)
admin.site.register(Storage)
