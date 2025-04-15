# server/auth.py

def check_user_permissions(user):

    user_permissions = {
        'admin': 'admin',
        'chief': 'chief',
        'user': 'user'
    }

    if user not in user_permissions:
        return False


    return user_permissions[user] in ['admin', 'chief']
