from functools import wraps
from flask import redirect, url_for, make_response
from flask_login import current_user


def check_authentication(redirect_route):
    """Decorator that redirects authenticated users to the specified route."""

    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user.is_authenticated:
                return redirect(url_for(redirect_route))
            return func(*args, **kwargs)

        return decorated_view

    return decorator


def prevent_cache(func):
    """Decorator that adds headers to prevent caching of the response."""

    @wraps(func)
    def decorated_view(*args, **kwargs):
        response = make_response(func(*args, **kwargs))
        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0"
        )
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "-1"
        return response

    return decorated_view
