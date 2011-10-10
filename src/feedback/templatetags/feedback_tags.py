from django import template

from feedback.forms import FeedbackForm


register = template.Library()

@register.inclusion_tag('feedback/feedback_form.html',
                        takes_context=True)
def feedback_form(context):
    user = context['user']

    feedback_initial = {}

    if user and user.is_authenticated():
        feedback_initial['name'] = getattr(user, 'soc_username', user.username)
        if user.email:
            feedback_initial['email'] = user.email

    return {'feedback_form': FeedbackForm(initial=feedback_initial)}


