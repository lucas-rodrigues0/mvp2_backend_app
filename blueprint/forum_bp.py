from flask_openapi3 import APIBlueprint
from flask_openapi3 import Tag


tag = Tag(name="Forum", description="Some Forum")


forum_bp = APIBlueprint(
    "/forum", __name__, url_prefix="/api", abp_tags=[tag], doc_ui=True
)


@forum_bp.get("/forum")
def get_forum():
    return {"message": "forum"}
