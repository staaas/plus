from social_auth.models import UserSocialAuth


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
        if soc is None:
            usr.soc_username = usr.username
            usr.soc_link = ''
            usr.soc_avatar = ''
            usr.soc_provider = ''
        elif soc.provider == 'twitter':
            usr.soc_username = soc.extra_data.get('screen_name') or usr.username
            usr.soc_link = 'http://twitter.com/%s' % soc.extra_data.get('screen_name') if \
                soc.extra_data.get('screen_name') else ''
            usr.soc_avatar = 'http://img.tweetimag.es/i/%s' % usr.soc_username
            usr.soc_provider = soc.provider
        elif soc.provider == 'facebook':
            usr.soc_username = ('%s %s' % (usr.first_name, usr.last_name)).strip() or usr.username
            usr.soc_link = 'https://www.facebook.com/profile.php?id=%s' % soc.uid
            usr.soc_avatar = 'http://graph.facebook.com/%s/picture' % soc.uid
            usr.soc_provider = soc.provider
        elif soc.provider == 'vkontakte-oauth2':
            usr.soc_username = ('%s %s' % (usr.first_name, usr.last_name)).strip() or usr.username
            usr.soc_link = 'https://vkontakte.ru/id%s' % soc.uid
            usr.soc_avatar = ''
            usr.soc_provider = 'vkontakte'
        elif soc.provider == 'openid':
            usr.soc_username = ('%s %s' % (usr.first_name, usr.last_name)).strip() or usr.username
            usr.soc_link = soc.uid
            usr.soc_avatar = ''
            usr.soc_provider = soc.provider
        else:
            usr.soc_link = ''
            usr.soc_avatar = ''
            usr.soc_provider = ''
            

    return users_list

def socialize_user(user):
    '''
    Socializes single user:
    adds attributes soc_link and soc_provider to the user and returns it.
    '''
    return socialize_users([user])[0]
    
