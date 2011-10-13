import time

from django.conf import settings
from django import forms
from django.utils.translation import ugettext as _
from django.utils.hashcompat import sha_constructor


ANY_SECURITY_SALT = getattr(settings,'SECRET_KEY', '')[1:10:2]

class SimpleSecurityForm(forms.Form):
    timestamp     = forms.IntegerField(widget=forms.HiddenInput)
    honeypot      = forms.CharField(required=False,
                                    label=_('If you enter anything in this field '\
                                            'your comment will be treated as spam'))

    def __init__(self, data=None, initial=None):
        if initial is None:
            initial = {}
        initial.update(self.generate_security_data())
        super(SimpleSecurityForm, self).__init__(data=data, initial=initial)

    def generate_security_data(self):
        """Generate a dict of security data for "initial" data."""
        timestamp = int(time.time())
        security_dict =   {
            'timestamp'     : str(timestamp),
        }
        return security_dict

    def clean_timestamp(self):
        """Make sure the timestamp isn't too far (> 2 hours) in the past."""
        ts = self.cleaned_data["timestamp"]
        if time.time() - ts > (2 * 60 * 60):
            raise forms.ValidationError("Timestamp check failed")
        return ts

    def clean_honeypot(self):
        """Check that nothing's been entered into the honeypot."""
        value = self.cleaned_data["honeypot"]
        if value:
            raise forms.ValidationError(self.fields["honeypot"].label)
        return value



FEEDBACK_MAX_LENGTH = getattr(settings,'FEEDBACK_MAX_LENGTH', 3000)

class FeedbackForm(SimpleSecurityForm):
    name = forms.CharField(label=_("Name"), max_length=50)
    email = forms.EmailField(label=_("E-mail"))
    text = forms.CharField(label=_('Feedback'),
                              max_length=FEEDBACK_MAX_LENGTH,
                              widget=forms.Textarea(attrs={'rows': 4}))

