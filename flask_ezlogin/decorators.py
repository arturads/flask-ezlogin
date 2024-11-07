from functools import wraps
from flask import redirect, url_for, make_response
from flask_login import current_user

def verifica_autenticacao(redirect_route="protected_route"):
    """Decorator que redireciona usuários autenticados para a rota especificada."""
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user.is_authenticated:
                return redirect(url_for(redirect_route))
            return func(*args, **kwargs)
        return decorated_view
    return decorator

def evitar_cache(func):
    """Decorator que adiciona cabeçalhos para evitar cache na resposta."""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        response = make_response(func(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return decorated_view
