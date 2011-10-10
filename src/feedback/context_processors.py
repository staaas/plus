from .forms import FeedbackForm


def feedback_form(request):
    user = getattr(request, 'user', None)
    feedback_initial = {}

    if user and user.is_authenticated():
        feedback_initial['name'] = getattr(user, 'soc_username', user.username)
        if user.email:
            feedback_initial['email'] = user.email

    return {'feedback_form': FeedbackForm(initial=feedback_initial)}
