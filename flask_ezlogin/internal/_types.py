from typing import NewType
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

Email = NewType("Email", str)

# Tipo personalizado para campos de senha
Password = NewType("Password", str)


class EzUser(UserMixin):
    _ez_email = ""
    _ez_password = ""

    @classmethod
    def __init_subclass__(cls, **kwargs):
        # Captura as anotações originais
        cls.__annotations_original__ = dict(cls.__annotations__)
        print(f"Anotações capturadas em {cls.__name__}: {cls.__annotations_original__}")

        # Cria atributos dinamicamente com prefixo _ez_
        for field_name, field_type in cls.__annotations_original__.items():
            prefixed_name = f"_ez_{field_type.__name__.lower()}"
            # Atribui o campo original da classe ao novo atributo prefixed_name
            setattr(cls, prefixed_name, field_name)
            print(f"Atributo '{prefixed_name}' criado em {cls.__name__}")

        super().__init_subclass__(**kwargs)

    def check_password(self, password_to_check: str) -> bool:
        hash_password = getattr(self, self._ez_password)
        print(f"Hash no banco de dados: {hash_password}")
        print(f"Senha em texto claro recebida: {password_to_check}")
        resultado = check_password_hash(hash_password, password_to_check)
        print(f"Resultado: {resultado}")
        return resultado

    def hash_password(self, password: str) -> Password:
        return Password(generate_password_hash(password))
