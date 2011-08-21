from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.forms import CommentDetailsForm

class CommentForm(CommentDetailsForm):
    email = forms.EmailField(label=_("Email address"), required=False)

def get_form():
    return CommentForm
