import functools

user = {"username": "Misty", "access_leveel": "guest"}


def make_secure(access_level):
    def decorator(func):
        @functools.wraps(func)
        def secure_funtion(*args, **kwargs):
            if user["access_level"] == access_level:
                return func(*args, **kwargs)
            else:
                return f"{user['username']} does not have {access_level} permissions."

        return secure_funtion
    return decorator


@make_secure("admin")
def get_admin_password():
    return "Misty: Me"
