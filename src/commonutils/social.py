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
            usr.soc_link = ''
            usr.soc_provider = ''
        else:
            usr.soc_link = soc.uid
            usr.soc_provider = soc.provider

    return users_list

def socialize_user(user):
    '''
    Socializes single user:
    adds attributes soc_link and soc_provider to the user and returns it.
    '''
    return socialize_users([user])[0]
    
