from django.contrib import admin

from .models import Command


class CommandAdmin(admin.ModelAdmin):
    pass


admin.site.register(Command, CommandAdmin)
