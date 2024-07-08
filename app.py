from os import environ as env
from dotenv import find_dotenv, load_dotenv
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth

from flask_openapi3 import OpenAPI, Info
from flask import redirect, session, url_for, request
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
        return {
            "user": "Logado",
            "cookie": request.cookies,
            "user_info": user.get("userinfo"),
        }
    else:
        return {"Fazer o login": "localhost:3000/login"}


app.register_api(searcher_bp)
app.register_api(forum_bp)
