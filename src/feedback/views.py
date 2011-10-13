import logging

from django.template import loader
from django.http import HttpResponse, Http404
from pyres import ResQ

from feedback.forms import FeedbackForm
from feedback.tasks import FeedbackTask


logger = logging.getLogger(__name__)

def submit_feedback(request):
    if request.method != 'POST':
        raise Http404

    try:
        form = FeedbackForm(request.POST or None)
        if form.is_valid():
            r = ResQ()
            r.enqueue(FeedbackTask, form.cleaned_data['name'],
                      form.cleaned_data['email'], form.cleaned_data['text'])
            return HttpResponse(status=200)
    
        # form is invalid
        return HttpResponse(
            loader.render_to_string('feedback/feedback_form_partial.html',
                                    {'feedback_form': form}),
            status=409)
    except Exception:
        logger.exception('')
        raise

