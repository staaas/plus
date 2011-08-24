from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.forms import CommentDetailsForm, COMMENT_MAX_LENGTH

class CommentForm(CommentDetailsForm):
    email = forms.EmailField(label=_("Email address"), required=False)
    comment       = forms.CharField(label=_('Comment'), widget=forms.Textarea({'class':'xxlarge', 'rows': 5}),
                                    max_length=COMMENT_MAX_LENGTH)


def get_form():
    return CommentForm
