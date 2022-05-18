from django.contrib import admin
from barkeeper.models import Event

class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Event, AuthorAdmin)