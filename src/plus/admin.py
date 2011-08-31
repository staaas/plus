from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug_display', 'creator', 'starts_at']
    fields = ['title', 'slug', 'language', 'description', 'creator',
              'starts_at', 'seats_number', 'created_at', 'url', 'logo']
    readonly_fields = ['slug', 'created_at']
    ordering = ['-starts_at']

    def has_change_permission(self, request, obj=None):
        change_perm = super(EventAdmin, self).has_change_permission(
            request, obj)

        # we do not care about changelist
        if obj is None:
            return change_perm

        # we've got a single object editing
        if change_perm:
            if request.user.has_perm('plus.can_moderate_all') or \
                    obj.creator == request.user:
                return True
        return False

    def slug_display(self, obj):
        return '<a href="%s">%s</a>' % \
            (reverse('show_event', args=[obj.slug]),
             obj.slug)
    slug_display.short_description = _(u'Internal link')
    slug_display.allow_tags = True

    def queryset(self, request):
        qs = super(EventAdmin, self).queryset(request)

        if not request.user.has_perm('plus.can_moderate_all'):
            qs = qs.filter(creator=request.user)

        return qs


admin.site.register(Event, EventAdmin)
