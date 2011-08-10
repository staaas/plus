import random
from django.db import models
from django.contrib.auth.models import User

UPLOAD_DIR = 'eventimg'

LANG_CHOICES = [(0, 'Belarussian'),
                (1, 'Russian'),]

LANG_CODES = {0: 'be',
              1: 'ru'}

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

class Event(models.Model):
    id = models.AutoField(primary_key = True)

    slug = models.SlugField(unique=True, max_length=40, default=random_slug)
    language = models.IntegerField(max_length=2, choices=LANG_CHOICES)
    creator = models.ForeignKey(User)

    created_at = models.DateTimeField(auto_now=True)
    starts_at = models.DateTimeField()

    title = models.CharField(max_length=150, default='')
    description = models.TextField(default='')
    url = models.CharField(max_length=256, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True, upload_to=UPLOAD_DIR)

    def __unicode__(self):
        return self.title

class EventAttendance(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
