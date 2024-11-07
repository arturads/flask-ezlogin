from flask_login import (
    login_required as flask_login_required,
    logout_user as flask_logout_user,
    login_user as flask_login_user,
)
from .decorators import check_authentication, prevent_cache


def login_required(func):
    """Wrapper for Flask-Login's login_required decorator."""
    return flask_login_required(func)


def login_user(user, remember=False, duration=None):
    """
    Wrapper for Flask-Login's login_user function.

    Parameters:
    - user: The user to be authenticated.
    - remember: Boolean to indicate if the login should persist after closing the browser.
    - duration: Duration of the login session (if remember=True).
    """
    flask_login_user(user, remember=remember, duration=duration)


def logout_user():
    """Wrapper for Flask-Login's logout_user function."""
    flask_logout_user()


__all__ = [
    "check_authentication",
    "prevent_cache",
    "login_required",
    "login_user",
    "logout_user",
]
