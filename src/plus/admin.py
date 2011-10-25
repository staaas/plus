from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug_display', 'creator', 'starts_at']
    ordering = ['-starts_at']
    readonly_fields = ['slug_display', 'created_at']

    # fieldsets will be defined in get_fieldsets
    add_fieldsets = (
        (None, {'fields': ('title', 'description', 'language')}),
        (_('Details'), {'fields': ('starts_at', 'seats_number', 'url', 'logo')}),
    )

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

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        extra_fields = ['created_at']
        if request.user.is_superuser:
            extra_fields = ['creator'] + extra_fields
        self.fieldsets = (
            (None, {'fields': ('title', 'slug_display', 'description', 'language')}),
            (_('Details'), {'fields': ('starts_at', 'seats_number', 'url', 'logo')}),
            (_('Extra'), {'fields': extra_fields}),
            )

        return super(EventAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during event creation
        """
        defaults = {}
        if obj is None:
            defaults.update({
                'fields': admin.util.flatten_fieldsets(self.add_fieldsets),
            })
        defaults.update(kwargs)
        return super(EventAdmin, self).get_form(request, obj, **defaults)

    def save_model(self, request, obj, form, change): 
        ''' Adding current user on save if created_by is not defined '''
        instance = form.save(commit=False)

        if getattr(instance, 'creator', None) is None:
            instance.creator = request.user

        instance.save()
        form.save_m2m()
        return instance


admin.site.register(Event, EventAdmin)
