import random
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageModel


UPLOAD_DIR = 'posters'

SUPPORTED_LANGUAGES = [(0, 'be', 'Belarussian'),
                       (1, 'ru', 'Russian'),]
LANG_CHOICES = [(c, l) for c, s, l in SUPPORTED_LANGUAGES]
LANG_CODES = {c: s for c, s, l in SUPPORTED_LANGUAGES}

SLUG_ALPHABET = 'abcdefghijklmnopqrstuvwxyz'\
    '0123456789'
SLUG_LENGTH = 6
SLUG_TRY_TIMES = 15

def random_slug():
    for i in xrange(SLUG_TRY_TIMES):
        candidate = ''.join(
            random.choice(SLUG_ALPHABET) for j in xrange(SLUG_LENGTH))
        if Event.objects.filter(slug=candidate).count() == 0:
            return candidate
    raise Exception('Failed to generate slug in % trials' % SLUG_TRY_TIMES)    

class Event(ImageModel):
    id = models.AutoField(primary_key = True)

    slug = models.SlugField(unique=True, max_length=40, default=random_slug)
    language = models.IntegerField(max_length=2, choices=LANG_CHOICES)
    creator = models.ForeignKey(User)

    created_at = models.DateTimeField(auto_now_add=True)
    starts_at = models.DateTimeField()

    title = models.CharField(max_length=150, default='')
    description = models.TextField(default='')
    url = models.CharField(max_length=256, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True, upload_to=UPLOAD_DIR)
    seats_number = models.IntegerField(max_length=5, null=True, blank=True, default=None)

    def __unicode__(self):
        return self.title
    class Meta:
        permissions = (
            ("can_moderate_all", _(u"Can add, edit or delete any event")),
        )

    class IKOptions:
        # This inner class is where we define the ImageKit options for the model
        spec_module = 'plus.eventlogospecs'
        cache_dir = 'display'
        image_field = 'logo'

STATUS_SIGN_UP = 0
STATUS_REFUSE = 1
STATUS_SIGN_UP_AND_COME = 2
STATUS_SIGN_UP_BUT_DO_NOT_COME = 3

STATUS_CHOICES = [(STATUS_SIGN_UP,  _(u'Signed up')),
                  (STATUS_REFUSE, _(u'Refused')),
                  (STATUS_SIGN_UP_AND_COME, _(u'Signed up and came')),
                  (STATUS_SIGN_UP_BUT_DO_NOT_COME, _(u'Signed up but didn\'t come'))]

class EventAttendance(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(max_length=2, choices=STATUS_CHOICES, default=STATUS_SIGN_UP)
