from django.utils.translation import ugettext as _
from django import forms

from models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'url', 'logo',
                  'language', 'starts_at',)

class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'creator', 'description', 'url', 'logo',
                  'language', 'starts_at',)
