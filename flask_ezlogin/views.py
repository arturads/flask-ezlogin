from flask import (
    make_response,
    request,
    redirect,
    url_for,
    render_template,
    flash,
    Response,
)
from flask_login import login_user, logout_user
from typing import Callable, Dict, Optional, Type, Union
from urllib.parse import urlsplit
from wtforms import Form

from .internal._types import EzUser

from .enums import AuthMethod


def login_view(
    *,
    form_class: Type[Form],
    field_mapping: Optional[dict[str, str]] = None,
    auth_method: Union[AuthMethod, tuple[AuthMethod, dict[str, str]]],
    user_loader: Callable[[str], EzUser | None],
    template: str,
    redirect_authenticated: str,
    flash_unauthenticated: Optional[str] = None,
    flash_authenticated: Optional[str] = None,
) -> Response:
    """
    Simplified login view for Flask applications with flexible authentication methods.

    Parameters:
    - form_class: The form class to be used for login (e.g., LoginForm).
    - field_mapping: A dictionary mapping form field names to model field names (optional).
    - auth_method: An AuthMethod enum or a tuple (AuthMethod, custom field mapping).
    - user_loader: A function that takes an identifier (e.g., email or username) and returns a user instance or None.
    - template: Template path to render the login form.
    - redirect_authenticated: Route to redirect authenticated users.
    - redirect_unauthenticated: Route to redirect on failed login.
    - flash_unauthenticated: Optional message to flash on failed login.
    - flash_authenticated: Optional message to flash on successful authentication.

    Returns:
    - A Flask Response object with the appropriate redirection or rendered template.
    """
    form = form_class()

    # Construir os dados do modelo diretamente com o mapeamento
    field_mapping = field_mapping or {}
    model_data = {
        field_mapping.get(form_field, form_field): getattr(form, form_field).data
        for form_field in form._fields.keys()
    }
    print(f"model_data: {model_data}")

    # Resolver o método de autenticação e os campos necessários
    if isinstance(auth_method, tuple):
        method, custom_mapping = auth_method
        auth_fields = method.get_fields(custom_mapping)
    else:
        method = auth_method
        auth_fields = method.get_fields()

    print(f"auth_fields: {auth_fields}")

    if form.validate_on_submit():
        try:
            # Lógica de autenticação baseada no método
            if (
                method == AuthMethod.EMAIL_PASSWORD
                or method == AuthMethod.USERNAME_PASSWORD
            ):
                identifier = model_data[auth_fields["identifier"]]
                password = model_data[auth_fields["password"]]

                print(f"identifier: {identifier} e password: {password}")

                # Carregar o usuário pelo identificador
                user = user_loader(identifier)

                print(f"user: {user}")
                # Verificar senha
                if user is None or not user.check_password(password):
                    if flash_unauthenticated:  # Somente exibe a mensagem se definida
                        flash(flash_unauthenticated)
                    return make_response(render_template(template, form=form))

            elif method == AuthMethod.OAUTH2:
                token = model_data[auth_fields["token"]]

                # Carregar o usuário pelo token
                user = user_loader(token)

                if user is None:
                    if flash_unauthenticated:  # Somente exibe a mensagem se definida
                        flash(flash_unauthenticated)
                    return make_response(render_template(template, form=form))

            else:
                raise ValueError(f"Unsupported authentication method: {method}")

            # Logar o usuário
            remember = model_data.get(auth_fields.get("remember", "remember"), False)
            login_user(user, remember=remember)

            # Exibir mensagem de sucesso, se fornecida
            if flash_authenticated:
                flash(flash_authenticated)

            # Redirecionar para a próxima página ou página autenticada padrão
            next_page = request.args.get("next")
            if not next_page or urlsplit(next_page).netloc != "":
                next_page = url_for(redirect_authenticated)
            return make_response(redirect(next_page))
        except Exception as e:
            # Log de erro para debug (opcional)
            print(f"Error during login: {e}")
            if flash_unauthenticated:  # Somente exibe a mensagem se definida
                flash(flash_unauthenticated)
            return make_response(render_template(template, form=form))

    # Renderizar o template de login
    return make_response(render_template(template, form=form))


def logout_view(
    *,
    redirect_to: str,
    flash_message: Optional[str] = None,
) -> Response:
    """
    Simplified logout view for Flask applications.

    Parameters:
    - redirect_to: The route to redirect after logout.
    - flash_message: Optional message to flash after logout.
    """
    # Faz logout do usuário
    logout_user()

    # Mostra uma mensagem flash opcional
    if flash_message:
        flash(flash_message)

    # Redireciona para a rota especificada
    return make_response(redirect(url_for(redirect_to)))


def register_view(
    *,
    form_class: Type[Form],
    field_mapping: Optional[Dict[str, str]] = None,
    user_creator: Callable[[dict], None],
    template: str,
    redirect_success: str,
    flash_success: Optional[str] = None,
    flash_failure: Optional[str] = None,
) -> Response:
    """
    Simplified register view for Flask applications.

    Parameters:
    - form_class: The form class to be used for registration (e.g., CadastroForm).
    - field_mapping: An optional dictionary mapping model field names to form field names.
    - user_creator: A function that takes a dictionary of user data and saves the user.
    - template: Template path to render the registration form.
    - redirect_success: Route to redirect after successful registration.
    - flash_success: Optional message to flash on successful registration.
    - flash_failure: Optional message to flash on failed registration.

    Returns:
    - A Flask Response object with the appropriate redirection or rendered template.
    """
    form = form_class()

    # Construir os dados do modelo diretamente com o mapeamento
    field_mapping = field_mapping or {}
    model_data = {
        field_mapping.get(form_field, form_field): getattr(form, form_field).data
        for form_field in form._fields.keys()
    }
    print(f"model_data: {model_data}")

    if form.validate_on_submit():
        try:
            # Criar o usuário usando a função `user_creator`
            user_creator(model_data)

            # Mensagem de sucesso opcional
            if flash_success:
                flash(flash_success)

            return make_response(redirect(url_for(redirect_success)))
        except Exception as e:
            # Log de erro para debug (opcional)
            print(f"Error to create user: {e}")

            # Mensagem de falha opcional
            if flash_failure:
                flash(flash_failure)
            return make_response(render_template(template, form=form))

    # Renderizar o template de cadastro
    return make_response(render_template(template, form=form))
