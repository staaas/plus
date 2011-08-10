from django.contrib import admin
from models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'creator', 'starts_at']
    fields = ['title', 'slug', 'language', 'description', 'creator',
              'starts_at', 'created_at', 'url', 'logo']
    readonly_fields = ['slug', 'created_at']
    ordering = ['starts_at']
admin.site.register(Event, EventAdmin)
