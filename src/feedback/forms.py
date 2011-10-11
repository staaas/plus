from django.conf import settings
from django import forms
from django.contrib.comments.forms import CommentSecurityForm
from django.utils.translation import ugettext as _


FEEDBACK_MAX_LENGTH = getattr(settings,'FEEDBACK_MAX_LENGTH', 3000)

class FeedbackForm(forms.Form):
    name = forms.CharField(label=_("Name"), max_length=50)
    email = forms.EmailField(label=_("E-mail"))
    text = forms.CharField(label=_('Feedback'),
                              max_length=FEEDBACK_MAX_LENGTH,
                              widget=forms.Textarea(attrs={'rows': 4}))
