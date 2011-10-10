from django.template import loader
from django.http import HttpResponse, Http404

from feedback.forms import FeedbackForm

def submit_feedback(request):
#    if request.method != 'POST':
#        raise Http404

    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        HttpResponse(status=200)
    
    # form is invalid
    return HttpResponse(
        loader.render_to_string('feedback/feedback_form_partial.html',
                                {'feedback_form': form}),
        status=409)
    
    
