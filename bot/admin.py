from django.contrib import admin

from .models import Command, Bot


admin.site.register(Command)
admin.site.register(Bot)
