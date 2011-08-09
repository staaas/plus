import datetime

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect

from models import Event, EventAttendance
from commonutils.decorators import render_to

@render_to('plus/event.html')
def show_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    user = request.user
    
    attendances = list(EventAttendance.objects.filter(
            event=event).select_related('user'))

    return {'event': event,
            'curr_attendance': any(user.id == a.user.id for a in attendances),
            'future_event': event.starts_at > datetime.datetime.now(),
            'goers': sorted((a.user for a in attendances if \
                                 user.id != a.user.id),
                            key=lambda usr: usr.username)}


def event_plus(request, slug):
    event = get_object_or_404(Event, slug=slug)
    user = request.user

    if user.is_authenticated():
        att_count = EventAttendance.objects.filter(
            event=event, user=user).count()
        if att_count == 0:
            EventAttendance(event=event, user=user).save()

        return redirect(reverse('show_event', args=[slug]))

    raise Http404


def event_minus(request, slug):
    event = get_object_or_404(Event, slug=slug)
    user = request.user

    if user.is_authenticated():
        EventAttendance.objects.filter(
                event=event, user=user).delete()
        return redirect(reverse('show_event', args=[slug]))

    raise Http404
