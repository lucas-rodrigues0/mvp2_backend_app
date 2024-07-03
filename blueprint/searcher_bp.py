from flask_openapi3 import APIBlueprint
from flask_openapi3 import Tag


tag = Tag(name="Searcher", description="Some Searcher")


searcher_bp = APIBlueprint(
    "/searcher", __name__, url_prefix="/api", abp_tags=[tag], doc_ui=True
)


@searcher_bp.get("/searcher")
def get_searcher():
    return {"message": "searcher"}
