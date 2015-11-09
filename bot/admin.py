from django.contrib import admin

from .models import Command, Bot


class CommandAdmin(admin.ModelAdmin):
    pass


admin.site.register(Command, CommandAdmin)
admin.site.register(Bot)
