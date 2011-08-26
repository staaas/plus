from django import template
from django.contrib.auth.models import User

from commonutils.social import socialize_user, socialize_users


register = template.Library()

@register.filter
def annotate_users(comments):
    user_ids = set(c.user_id for c in comments)

    users_list = list(User.objects.filter(id__in=user_ids))
    users_list = socialize_users(users_list)
    users_dict = {u.id: u for u in users_list}

    for c in comments:
        user = users_dict.get(c.user_id)
        if user is None:
            # have we been hacked?
            comments.remove(c)
        else:
            c.user = user

    return comments

@register.inclusion_tag('plus/tags/comment_list.html',
                        takes_context=True)
def render_ncomment_list(context, event, comment_list, goer_id_set):
    for comment in comment_list:
        if comment.user_id in goer_id_set:
            comment.user_is_goer = True
    return {'comment_list': comment_list,
            'event': event,
            'request': context['request']}

