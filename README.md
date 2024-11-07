# flask-ezlogin

**flask-ezlogin** é um pacote que facilita a configuração de sistemas de login no Flask usando Flask-Login.

## Instalação

Você pode instalar diretamente do PyPI com:

```bash
pip install flask-ezlogin
```

### Funcionalidades

login_required: Um wrapper para o decorator login_required do Flask-Login, que restringe o acesso a rotas protegidas para usuários autenticados.
check_authentication: Redireciona o usuário autenticado para uma rota protegida se ele já estiver logado.
prevent_cache: Adiciona cabeçalhos para evitar cache em páginas sensíveis, como as páginas de login e cadastro.
login_user: Um wrapper para a função login_user do Flask-Login, que permite autenticar o usuário no sistema.
logout_user: Um wrapper para a função logout_user do Flask-Login, que permite deslogar o usuário.

Aqui estão alguns exemplos práticos de como usar os decorators e funções oferecidos pelo flask-ezlogin.

1. Proteger uma Rota com login_required
   Use login_required para restringir o acesso a uma rota apenas para usuários autenticados.

```
from flask import Flask, redirect, url_for
from flask_ezlogin import login_required, logout_user

app = Flask(**name**)

@app.route("/protected")
@login_required
def protected():
return "Esta é uma rota protegida."

@app.route("/logout")
@login_required
def logout():
logout_user()
return redirect(url_for("index"))
```

2. Redirecionar Usuários Autenticados com check_authentication
   Use check_authentication para redirecionar usuários já autenticados para uma rota protegida. Isso é útil, por exemplo, na página de login.

from flask import Flask, render_template
from flask_ezlogin import check_authentication, prevent_cache

app = Flask(**name**)

@app.route("/login")
@check_authentication("protected") # Redireciona para /protected se o usuário já estiver logado
@prevent_cache # Evita cache para essa página
def login():
return render_template("login.html")

3. Evitar Cache com prevent_cache
   O decorator prevent_cache adiciona cabeçalhos para garantir que o navegador não armazene a página em cache.

@app.route("/register")
@prevent_cache
def register():
return render_template("register.html")

4. Fazer Login com login_user
   Use login_user para autenticar um usuário no sistema. Esse método é um wrapper para a função login_user do Flask-Login, com os mesmos parâmetros, facilitando o uso direto a partir do pacote.

from flask_ezlogin import login_user
from flask_login import UserMixin

# Suponha que `user` seja uma instância de uma classe de usuário autenticável

login_user(user, remember=True) # Realiza o login e mantém a sessão após o fechamento do navegador

5. Fazer Logout com logout_user
   Use logout_user para deslogar o usuário autenticado. Esse método é um wrapper para a função logout_user do Flask-Login.

from flask_ezlogin import logout_user

@app.route("/logout")
def logout():
logout_user()
return redirect(url_for("index"))

### Contribuição

Contribuições são bem-vindas! Se você encontrar problemas, tiver ideias para novas funcionalidades ou melhorias, sinta-se à vontade para abrir um pull request ou relatar problemas no repositório GitHub.

### Licença

Este projeto é licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.
