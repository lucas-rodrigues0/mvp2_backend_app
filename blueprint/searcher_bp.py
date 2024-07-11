from os import environ as env
from dotenv import find_dotenv, load_dotenv
import requests

from flask_openapi3 import APIBlueprint
from flask_openapi3 import Tag

from schemas import QuerySchema, SearcherResponse
from logger import logger

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

searcher_api_url = env.get("SEARCH_API_URL")
tag = Tag(name="Full Text Searcher API", description="Some Searcher")

searcher_bp = APIBlueprint(
    "searcher", __name__, url_prefix="/api", abp_tags=[tag], doc_ui=True
)


@searcher_bp.get("/searcher", responses={"200": SearcherResponse})
def get_searcher(query: QuerySchema):
    """Rota para realizar uma busca de texto completo no serviço Full Text Searcher API.
    É utilizado o paramêtro de query '?term=' com o termo a ser buscado no serviço.
    ex: term='direito moradia' para buscar pelos termos 'direito' e/ou 'moradia'.
    """
    formatted_url = searcher_api_url + f"/searcher?query={query.term}"
    response = requests.get(url=formatted_url)
    if response.status_code == 200:
        searcher_data = response.json()
        return searcher_data["data"]

    logger.warning(
        f"Erro na busca pelo termo {query.term}. Response status code: {response.status_code}."
    )
    return {"status_code": response.status_code, "error": "error"}
