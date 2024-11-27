from flask import Flask
from flask_login import (
    LoginManager,
    login_required as flask_login_required,
)
from typing import Callable, Optional

from .enums import AuthMethod
from .decorators import check_authentication, prevent_cache
from .views import login_view, logout_view, register_view

# Instância global do LoginManager
login_manager = LoginManager()


def init_login(
    app: Flask,
    user_loader_callback: Callable[[str], Optional[object]],
    login_view: str,
    login_message: str = "Please, login to acess these page.",
):
    """
    Inicializa o LoginManager com a aplicação Flask.

    Parameters:
    - app: A aplicação Flask.
    - user_loader_callback: Função para carregar o usuário, recebendo o user_id.
    - login_view: Rota de login.
    - login_message: Mensagem exibida para usuários não autenticados.
    """
    # Inicializa o login_manager com o app Flask
    login_manager.init_app(app)

    # Configura as propriedades após a inicialização
    login_manager.login_view = login_view
    login_manager.login_message = login_message
    login_manager.user_loader(user_loader_callback)


def login_required(func):
    """Envolve o login_required do Flask-Login."""
    return flask_login_required(func)


__all__ = [
    "init_login",
    "login_required",
    "login_view",
    "logout_view",
    "register_view",
    "check_authentication",
    "prevent_cache",
    "AuthMethod",
]
