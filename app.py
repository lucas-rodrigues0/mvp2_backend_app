from os import environ as env
from dotenv import find_dotenv, load_dotenv
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth

from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, session, url_for, request
from flask_cors import CORS

from logger import logger
from blueprint import searcher_bp, forum_bp


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


info = Info(title="MVP2 Backend APP", version="1.0.0")
auth_tag = Tag(
    name="Autenticação Auth0",
    description="Rotas para efetuar o Login e o Logout através do provedor Auth0",
)

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


@app.get("/docs")
def get_documentation():
    """Redireciona para a rota das documetações fornecidas pelo flask-openapi"""
    return redirect("/openapi")


@app.get("/login", tags=[auth_tag])
def login():
    """Redireciona para o provedor de autenticação do Auth0.
    Toda autenticação fica na responsabilidade do provedor.
    Assim como o armazenamento das informações do usuário
    """
    logger.debug("Redireciona para login no provedor Auth0.")
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    """Rota de retorno do provedor Auth0.
    Nessa rota o token de acesso e as informações de usuário são armazenados no
    cookie session do flask para manter o usuário autenticado.
    """
    token = oauth.auth0.authorize_access_token()
    logger.debug("Adiciona info de usuário logado no session cookie.")
    session["user"] = token
    return redirect("/")


@app.get("/logout", tags=[auth_tag])
def logout():
    """Rota para limpar as informações de usuário autenticado do cookie session.
    Depois disso o usuário não estará mais autenticado.
    """
    session.clear()
    logger.debug("Limpa o session cookie de usuario que estava logado.")
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


@app.get("/")
def home():
    """Essa rota apresenta as informações de usuário caso ele esteja autenticado.
    Se a variavel DEV_ENV estiver setada, apresenta ainda o cookie que deve ser
    enviado pelo usuário autenticado. Esse cookie que possui as informações
    necessária sobre o usuário para algumas rotas.
    """
    if session.get("user"):
        cookie = "******"
        if bool(env.get("DEV_ENV", None)):
            cookie = request.cookies
        return {
            "user": "Autenticado por Auth0",
            "cookie": cookie,
            "user_info": session.get("user").get("userinfo"),
        }
    else:
        return {"Fazer o login": "/login"}


app.register_api(searcher_bp)
app.register_api(forum_bp)
