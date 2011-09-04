from datetime import datetime
from hashlib import sha1

from django.conf import settings
from social_auth.models import UserSocialAuth

DEFAULT_AVATAR = getattr(settings, 'DEFAULT_SOCIAL_AVATAR', '')

def get_avatarizator_key():
    key_src = settings.AVATARIZATOR_KEY + datetime.now().strftime('%Y%m%d%H')
    return sha1(key_src).hexdigest()

def get_avatarizator_link(provider, uid, key=None):
    '''
    Link to avatarizator service.
    '''
    if not provider or not uid or not uid.isdigit():
        return DEFAULT_AVATAR
    if key is None:
        key = get_avatarizator_key()
    return settings.AVATARIZATOR_URL % {'provider': provider,
                                        'uid': uid,
                                        'key': key}

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

    avatarizator_key = get_avatarizator_key()
    
    for usr in users_list:
        soc = soc_dict.get(usr.id)

        # default values
        soc_username = usr.username
        soc_link = ''
        soc_provider = ''
        soc_uid = ''

        if soc is None:
            pass
        elif soc.provider == 'twitter':
            try:
                screen_name = soc.extra_data.get('screen_name')
            except (TypeError, ValueError, AttributeError):
                screen_name = None
            soc_username = screen_name or usr.username
            soc_link = 'http://twitter.com/%s' % screen_name if \
                screen_name else ''
            soc_uid = soc.uid
            soc_provider = soc.provider
        elif soc.provider == 'facebook':
            soc_username = ('%s %s' % (usr.first_name, usr.last_name)).strip() or usr.username
            soc_link = 'https://www.facebook.com/profile.php?id=%s' % soc.uid
            soc_uid = soc.uid
            soc_provider = soc.provider
        elif soc.provider == 'vkontakte-oauth2':
            soc_username = ('%s %s' % (usr.first_name, usr.last_name)).strip() or usr.username
            soc_link = 'https://vkontakte.ru/id%s' % soc.uid
            soc_provider = 'vkontakte'
            soc_uid = soc.uid
            usr.vk_id = soc.uid
        elif soc.provider == 'openid':
            soc_username = ('%s %s' % (usr.first_name, usr.last_name)).strip() or usr.username
            soc_link = soc.uid
            soc_uid = soc.uid
            soc_provider = soc.provider

        usr.soc_username = soc_username
        usr.soc_link = soc_link
        usr.soc_avatar = get_avatarizator_link(soc_provider, soc_uid, avatarizator_key)
        usr.soc_provider = soc_provider

    return users_list

def socialize_user(user):
    '''
    Socializes single user:
    adds attributes soc_link and soc_provider to the user and returns it.
    '''
    return socialize_users([user])[0]
    
