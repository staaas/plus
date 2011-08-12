from django import template
from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth

register = template.Library()

def annotate_users(comments):
    user_ids = set(c.user_id for c in comments)

    users_list = list(User.objects.filter(id__in=user_ids))
    users_dict = {u.id: u for u in users_list}

    soc_list = list(UserSocialAuth.objects.filter(
                user__id__in=user_ids).select_related())
    soc_dict = {s.user.id: s for s in soc_list}

    for c in comments:
        user_id = c.user_id
        user = users_dict.get(user_id)
        soc = soc_dict.get(user_id)
        if user is None:
            # have we been hacked?
            comments.remove(c)
        elif soc is None:
            c.user = user
            c.user.soc_link = ''
            c.user.soc_provider = ''
        else:
            c.user = user
            c.user.soc_link = soc.uid
            c.user.soc_provider = soc.provider

    return comments

register.filter(annotate_users)
