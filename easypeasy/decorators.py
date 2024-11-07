from functools import wraps
from flask import redirect, url_for
from flask_login import current_user
from flask import make_response


def verifica_autenticacao(redirect_route):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user.is_authenticated:
                # Redireciona para a rota protegida se o usuário já estiver autenticado
                return redirect(url_for(redirect_route))
            return func(*args, **kwargs)

        return decorated_view

    return decorator


def evitar_cache(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        response = make_response(func(*args, **kwargs))
        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
        )
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "-1"
        return response

    return decorated_view
