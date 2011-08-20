from django.conf import settings
from social_auth.models import UserSocialAuth

DEFAULT_AVATAR = getattr(settings, 'DEFAULT_SOCIAL_AVATAR', '')

def socialize_users(users_list):
    '''
    Socializes a list of users:
    adds attributes soc_link and soc_provider to each user in @users_list.

    Returns the "socialized" list but also modifies @users_list.
    '''
    user_ids = [u.id for u in users_list]

    soc_list = list(UserSocialAuth.objects.filter(
                user__id__in=user_ids).select_related())
    soc_dict = {s.user.id: s for s in soc_list}

    for usr in users_list:
        soc = soc_dict.get(usr.id)

        # default values
        soc_username = usr.username
        soc_link = ''
        soc_avatar = DEFAULT_AVATAR
        soc_provider = ''

        if soc is None:
            pass
        elif soc.provider == 'twitter':
            screen_name = soc.extra_data.get('screen_name')
            soc_username = screen_name or usr.username
            soc_link = 'http://twitter.com/%s' % screen_name if \
                screen_name else ''
            soc_avatar = 'http://img.tweetimag.es/i/%s' % screen_name if \
                screen_name else DEFAULT_AVATAR
            soc_provider = soc.provider
        elif soc.provider == 'facebook':
            soc_username = ('%s %s' % (usr.first_name, usr.last_name)).strip() or usr.username
            soc_link = 'https://www.facebook.com/profile.php?id=%s' % soc.uid
            soc_avatar = 'http://graph.facebook.com/%s/picture' % soc.uid
            soc_provider = soc.provider
        elif soc.provider == 'vkontakte-oauth2':
            soc_username = ('%s %s' % (usr.first_name, usr.last_name)).strip() or usr.username
            soc_link = 'https://vkontakte.ru/id%s' % soc.uid
            soc_provider = 'vkontakte'
        elif soc.provider == 'openid':
            soc_username = ('%s %s' % (usr.first_name, usr.last_name)).strip() or usr.username
            soc_link = soc.uid
            soc_provider = soc.provider

        usr.soc_username = soc_username
        usr.soc_link = soc_link
        usr.soc_avatar = soc_avatar
        usr.soc_provider = soc_provider

    return users_list

def socialize_user(user):
    '''
    Socializes single user:
    adds attributes soc_link and soc_provider to the user and returns it.
    '''
    return socialize_users([user])[0]
    
