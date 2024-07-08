from os import environ as env
from dotenv import find_dotenv, load_dotenv
import requests

from flask_openapi3 import APIBlueprint
from flask_openapi3 import Tag

from schemas import QuerySchema, SearcherResponse

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

searcher_api_url = env.get("SEARCH_API_URL")

tag = Tag(name="Searcher", description="Some Searcher")


searcher_bp = APIBlueprint(
    "/searcher", __name__, url_prefix="/api", abp_tags=[tag], doc_ui=True
)


@searcher_bp.get("/searcher", responses={"200": SearcherResponse})
def get_searcher(query: QuerySchema):

    formatted_url = searcher_api_url + f"/searcher?query={query.term}"
    response = requests.get(url=formatted_url)
    if response.status_code == 200:
        searcher_data = response.json()
        return searcher_data["data"]

    return {"status_code": response.status_code, "error": "error"}
