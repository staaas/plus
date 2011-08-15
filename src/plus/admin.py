from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug_display', 'creator', 'starts_at']
    fields = ['title', 'slug', 'language', 'description', 'creator',
              'starts_at', 'created_at', 'url', 'logo']
    readonly_fields = ['slug', 'created_at']
    ordering = ['starts_at']

    def slug_display(self, obj):
        return '<a href="%s">%s</a>' % \
            (reverse('show_event', args=[obj.slug]),
             obj.slug)
    slug_display.verbose_name = _(u'Link')
    slug_display.allow_tags = True

admin.site.register(Event, EventAdmin)
