from os import environ as env
from dotenv import find_dotenv, load_dotenv
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth

from flask_openapi3 import OpenAPI, Info
from flask import redirect, session, url_for
from flask_cors import CORS


from blueprint import searcher_bp, forum_bp


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


info = Info(title="CF searcher API", version="1.0.0")

app = OpenAPI(__name__, info=info)
CORS(app)

app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


@app.route("/")
def home():
    user = session.get("user")
    if user:
        return {"message": user.get("userinfo")}
    else:
        return redirect("/login")


app.register_api(searcher_bp)
app.register_api(forum_bp)


# home_tag = Tag(
#     name="Documentação",
#     description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
# )
# account_tag = Tag(
#     name="Accounts", description="Autenticação e adição de usuarios (account) à base"
# )


# @app.get("/", tags=[home_tag])
# def home():
#     """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
#     return redirect("/openapi")


# @app.post(
#     "/account/register",
#     tags=[account_tag],
#     responses={"200": AccountToken, "409": ErrorSchema, "400": ErrorSchema},
# )
# def register_account(body: AccountSchema):
#     """Adiciona um novo Usuário à base de dados
#     Retorna uma representação do usuário definido no schema.
#     """
#     data = request.get_json()
#     email = data.get("email")
#     username = data.get("username")
#     password = data.get("password")

#     if not username or not email or not password:
#         error_msg = "Nome de usuário, email e senha são necessários para registro"
#         logger.warning(f"Erro ao adicionar usuario. {error_msg}")
#         return {"data": {"message": error_msg}}, 409

#     account = Accounts(username=username, email=email, password=password)
#     logger.debug(f"Adicionando usuario de nome: '{account.username}'")

#     try:
#         session = Session()
#         session.add(account)
#         session.commit()
#         data = {
#             "account_id": str(account.account_id),
#             "username": account.username,
#             "email": account.email,
#         }

#         logger.debug(f"Adicionado usuário de nome: '{account.username}'")

#         # Usa os dados necessários do usuário para a codificação do token JWT
#         token = jwt_encode(data)

#         return {"data": {"token": token, "account_id": str(account.account_id)}}, 200

#     except IntegrityError as e:
#         error_msg = "Usuário de mesmo email já salvo na base"
#         logger.warning(
#             f"Erro ao adicionar usuario '{account.username} com o email {account.email}', {error_msg}"
#         )
#         return {"data": {"message": error_msg}}, 409

#     except Exception as e:
#         error_msg = "Não foi possível salvar novo item"
#         logger.warning(f"Erro ao adicionar usuário '{account.username}', {error_msg}")
#         return {"data": {"message": error_msg}}, 400


# @app.post(
#     "/account/login",
#     tags=[account_tag],
#     responses={"200": AccountToken, "403": ErrorSchema, "404": ErrorSchema},
# )
# def signin_account(body: AccountAuthForm):
#     """Faz a busca do usuarios cadastrado e autentica o password"""
#     data = request.get_json()
#     email = data.get("email")
#     password = data.get("password")

#     logger.debug(f"Login de usuário com email: {email}")

#     session = Session()
#     account = session.query(Accounts).filter(Accounts.email == email).first()

#     if not account:
#         return {"data": {"message": "Usuário não encontrado pelo email"}}, 404
#     elif password != account.password:
#         return {"data": {"message": "Senha inválida"}}, 403
#     else:
#         # Extrai os dados necessários do usuário para a codificação do token JWT
#         encode_data = {
#             "account_id": str(account.account_id),
#             "username": account.username,
#             "email": account.email,
#         }
#         token = jwt_encode(encode_data)

#         return {"data": {"token": token, "account_id": str(account.account_id)}}, 200
