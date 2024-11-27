from enum import Enum


class AuthMethod(Enum):
    EMAIL_PASSWORD = {
        "identifier": "email",
        "password": "password",
        "remember": "remember",
    }
    USERNAME_PASSWORD = {
        "identifier": "username",
        "password": "password",
        "remember": "remember",
    }
    OAUTH2 = {"token": "access_token"}

    def get_fields(self, custom_mapping=None):
        """
        Retorna os campos necessários para o método de autenticação.

        Parameters:
        - custom_mapping: Um dicionário com campos customizados.

        Returns:
        - Um dicionário com os campos mapeados.
        """
        fields = self.value.copy()
        if custom_mapping:
            fields.update(custom_mapping)
        return fields
