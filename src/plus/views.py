import datetime
import random

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.utils import translation
from django.contrib.auth import logout as auth_logout

from models import Event, EventAttendance, LANG_CODES
from commonutils.decorators import render_to
from commonutils.social import socialize_user, socialize_users

@render_to('plus/event.html')
def show_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    translation.activate(LANG_CODES[event.language])

    user = socialize_user(request.user)
    
    attendances = list(EventAttendance.objects.filter(
            event=event).select_related('user'))

    goers = [a.user for a in attendances if \
                        user.id != a.user.id]
    random.shuffle(goers)
    goers = socialize_users(goers)

    return {'Content-Language': translation.get_language(),
            'event': event,
            'curr_attendance': any(user.id == a.user.id for a in attendances),
            'future_event': event.starts_at > datetime.datetime.now(),
            'goers': goers}


def event_plus(request, slug):
    event = get_object_or_404(Event, slug=slug,
                              starts_at__gt=datetime.datetime.now())
    user = request.user

    if user.is_authenticated():
        att_count = EventAttendance.objects.filter(
            event=event, user=user).count()
        if att_count == 0:
            EventAttendance(event=event, user=user).save()

    return redirect(reverse('show_event', args=[slug]))


def event_minus(request, slug):
    event = get_object_or_404(Event, slug=slug,
                              starts_at__gt=datetime.datetime.now())
    user = request.user

    if user.is_authenticated():
        EventAttendance.objects.filter(
                event=event, user=user).delete()
    return redirect(reverse('show_event', args=[slug]))

def event_logout(request, slug):
    """Logs user out"""
    auth_logout(request)
    return redirect(reverse('show_event', args=[slug]))
