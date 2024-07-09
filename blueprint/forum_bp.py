from os import environ as env
from dotenv import find_dotenv, load_dotenv
import requests
from flask_openapi3 import APIBlueprint
from flask_openapi3 import Tag
from flask import session

from logger import logger
from schemas import (
    ByUserPathSchema,
    ByPeriodQueryParamSchema,
    ArticlePathSchema,
    CommentPathSchema,
    AddArticleBodySchema,
    UpdateArticleBodySchema,
    AddCommentBodySchema,
    UpdateCommentBodySchema,
    GetArticlesResponse,
    GetArticleByIdResponse,
    GetArticleByUserResponse,
    GetArticleByPeriodResponse,
    GetCommentsResponse,
    GetCommentByIdResponse,
    GetCommentByUserIdResponse,
    GetCommentByPeriodResponse,
    AddArticleResponse,
    RemoveArticleResponse,
    UpdateArticleResponse,
    AddCommentResponse,
    RemoveCommentResponse,
    UpdateCommentResponse,
    ErrorSchema,
)
from queries import (
    articles_query,
    article_by_id_query,
    articles_by_user_id_query,
    articles_by_period_query,
    comments_query,
    comment_by_id_query,
    comments_by_user_id_query,
    comments_by_period_query,
    add_article_mutation,
    remove_article_mutation,
    update_article_mutation,
    add_comment_mutation,
    remove_comment_mutation,
    update_comment_mutation,
)


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


forum_api_url = env.get("FORUM_API_URL")

tag = Tag(name="Forum", description="Some Forum")


forum_bp = APIBlueprint(
    "/forum",
    __name__,
    url_prefix="/api",
    abp_tags=[tag],
    abp_responses={400: ErrorSchema},
    doc_ui=True,
)


@forum_bp.get("/articles", responses={"200": GetArticlesResponse})
def get_articles():
    logger.debug("Buscando todos artigos existentes.")
    response = requests.post(url=forum_api_url, json={"query": articles_query})
    article_data = response.json()

    if article_data.get("errors"):
        logger.warning(f"Erro na busca de artigos: {article_data.get('errors')}.")
        return article_data, 400

    return article_data["data"], 200


@forum_bp.get("/articles/id/<article_id>", responses={"200": GetArticleByIdResponse})
def get_article_by_id(path: ArticlePathSchema):
    logger.debug("Buscando artigo pelo seu ID.")
    variables = {"articleID": path.article_id}

    response = requests.post(
        url=forum_api_url, json={"query": article_by_id_query, "variables": variables}
    )
    article_data = response.json()

    if article_data.get("errors"):
        logger.warning(f"Erro na busca de artigos: {article_data.get('errors')}.")
        return article_data, 400

    return article_data["data"], 200


@forum_bp.get("/articles/user/<user_id>", responses={"200": GetArticleByUserResponse})
def get_article_by_user_id(path: ByUserPathSchema):
    logger.debug("Buscando artigo pelo ID do usuário.")
    variables = {"userID": path.user_id}

    response = requests.post(
        url=forum_api_url,
        json={"query": articles_by_user_id_query, "variables": variables},
    )
    article_data = response.json()

    if article_data.get("errors"):
        logger.warning(f"Erro na busca de artigos: {article_data.get('errors')}.")
        return article_data, 400

    return article_data["data"], 200


@forum_bp.get("/articles/period", responses={"200": GetArticleByPeriodResponse})
def get_article_by_period(query: ByPeriodQueryParamSchema):
    logger.debug("Buscando artigo pelo periodo em que foi criado.")
    variables = {"initialDate": query.initialDate, "endDate": query.endDate}

    response = requests.post(
        url=forum_api_url,
        json={"query": articles_by_period_query, "variables": variables},
    )
    article_data = response.json()

    if article_data.get("errors"):
        logger.warning(f"Erro na busca de artigos: {article_data.get('errors')}.")
        return article_data, 400

    return article_data["data"], 200


@forum_bp.get("/comments", responses={"200": GetCommentsResponse})
def get_comments():
    logger.debug("Buscando comentários existentes.")
    response = requests.post(url=forum_api_url, json={"query": comments_query})
    comment_data = response.json()

    if comment_data.get("errors"):
        logger.warning(f"Erro na busca de comentários: {comment_data.get('errors')}.")
        return comment_data, 400

    return comment_data["data"], 200


@forum_bp.get("/comments/id/<comment_id>", responses={"200": GetCommentByIdResponse})
def get_comment_by_id(path: CommentPathSchema):
    logger.debug("Buscando comentário pelo seu ID.")
    variables = {"commentID": path.comment_id}

    response = requests.post(
        url=forum_api_url, json={"query": comment_by_id_query, "variables": variables}
    )
    comment_data = response.json()

    if comment_data.get("errors"):
        logger.warning(f"Erro na busca de comentários: {comment_data.get('errors')}.")
        return comment_data, 400

    return comment_data["data"], 200


@forum_bp.get("/comments/user/<user_id>", responses={"200": GetCommentByUserIdResponse})
def get_comments_by_user_id(path: ByUserPathSchema):
    logger.debug("Buscando comentário pelo ID do usuário.")
    variables = {"userID": path.user_id}

    response = requests.post(
        url=forum_api_url,
        json={"query": comments_by_user_id_query, "variables": variables},
    )
    comment_data = response.json()

    if comment_data.get("errors"):
        logger.warning(f"Erro na busca de comentários: {comment_data.get('errors')}.")
        return comment_data, 400

    return comment_data["data"], 200


@forum_bp.get("/comments/period", responses={"200": GetCommentByPeriodResponse})
def get_comments_by_period(query: ByPeriodQueryParamSchema):
    logger.debug("Buscando comentário pelo periodo em que foi criado.")
    variables = {"initialDate": query.initialDate, "endDate": query.endDate}

    response = requests.post(
        url=forum_api_url,
        json={"query": comments_by_period_query, "variables": variables},
    )
    comment_data = response.json()

    if comment_data.get("errors"):
        logger.warning(f"Erro na busca de comentários: {comment_data.get('errors')}.")
        return comment_data, 400

    return comment_data["data"], 200


@forum_bp.post("/article", responses={"200": AddArticleResponse})
def add_article(body: AddArticleBodySchema):
    user = session.get("user")
    if not user:
        logger.warning("Usuário não logado!")
        return {"error": "User not logged in!"}, 403

    user_info = user.get("userinfo")
    user_data = {
        "userEmail": user_info.get("email"),
        "userID": user_info.get("sub"),
        "userNickname": user_info.get("nickname"),
    }

    variables = {
        "content": body.content,
        "title": body.title,
    }
    variables.update(user_data)

    logger.debug(f"Adicionando artigo de usuário '{user_data.get('userNickname')}'")
    response = requests.post(
        url=forum_api_url, json={"query": add_article_mutation, "variables": variables}
    )
    article_data = response.json()
    result = article_data.get("data")
    if article_data.get("errors") or result.get("addArticle").get("errors"):
        erro_msg = article_data.get("errors") or result.get("addArticle").get("errors")
        logger.warning(f"Erro ao adicionar artigo: {erro_msg}")

        return article_data, 400

    logger.debug(f"Artigo de {user_data.get('userNickname')} adicionado com sucesso.")
    return article_data["data"], 200


@forum_bp.delete("/article/<article_id>", responses={"200": RemoveArticleResponse})
def remove_article(path: ArticlePathSchema):
    user = session.get("user")
    if not user:
        logger.warning("Usuário não logado!")
        return {"error": "User not logged in!"}, 403

    user_info = user.get("userinfo")
    user_data = {
        "userEmail": user_info.get("email"),
        "userID": user_info.get("sub"),
        "userNickname": user_info.get("nickname"),
    }

    variables = {"articleID": path.article_id}
    variables.update(user_data)

    logger.debug(
        f"Removendo artigo {path.article_id} de usuário {user_data.get('userNickname')}"
    )
    response = requests.post(
        url=forum_api_url,
        json={"query": remove_article_mutation, "variables": variables},
    )
    article_data = response.json()
    result = article_data.get("data")
    if article_data.get("errors") or result.get("removeArticle").get("errors"):
        erro_msg = article_data.get("errors") or result.get("removeArticle").get(
            "errors"
        )
        logger.warning(f"Erro ao remover artigo: {erro_msg}")

        return article_data, 400

    logger.debug(f"Artigo de {user_data.get('userNickname')} removido com sucesso.")
    return article_data["data"], 200


@forum_bp.put("/article/<article_id>", responses={"200": UpdateArticleResponse})
def update_article(path: ArticlePathSchema, body: UpdateArticleBodySchema):
    user = session.get("user")
    if not user:
        logger.warning("Usuário não logado!")
        return {"error": "User not logged in!"}, 403

    user_info = user.get("userinfo")
    user_data = {
        "userEmail": user_info.get("email"),
        "userID": user_info.get("sub"),
        "userNickname": user_info.get("nickname"),
    }

    variables = {
        "articleID": path.article_id,
        "content": body.content or None,
        "title": body.title or None,
    }
    variables.update(user_data)

    logger.debug(
        f"Atualizando artigo {path.article_id} de usuário {user_data.get('userNickname')}"
    )
    response = requests.post(
        url=forum_api_url,
        json={"query": update_article_mutation, "variables": variables},
    )
    article_data = response.json()
    result = article_data.get("data")
    if article_data.get("errors") or result.get("updateArticle").get("errors"):
        erro_msg = article_data.get("errors") or result.get("updateArticle").get(
            "errors"
        )
        logger.warning(f"Erro ao atualizar artigo: {erro_msg}")

        return article_data, 400

    logger.debug(f"Artigo de {user_data.get('userNickname')} atualizado com sucesso.")
    return result, 200


@forum_bp.post("/comment", responses={"200": AddCommentResponse})
def add_comment(body: AddCommentBodySchema):
    user = session.get("user")
    if not user:
        logger.warning("Usuário não logado!")
        return {"error": "User not logged in!"}, 403

    user_info = user.get("userinfo")
    user_data = {
        "userEmail": user_info.get("email"),
        "userID": user_info.get("sub"),
        "userNickname": user_info.get("nickname"),
    }

    variables = {
        "articleID": body.article_id,
        "content": body.content,
        "isReply": body.is_reply or False,
        "commentReply": body.comment_reply or None,
    }
    variables.update(user_data)

    logger.debug(f"Adicionando comentário de usuário {user_data.get('userNickname')}")
    response = requests.post(
        url=forum_api_url, json={"query": add_comment_mutation, "variables": variables}
    )
    comment_data = response.json()
    result = comment_data.get("data")
    if comment_data.get("errors") or result.get("addComment").get("errors"):
        erro_msg = comment_data.get("errors") or result.get("addComment").get("errors")
        logger.warning(f"Erro ao adicionar comentário: {erro_msg}")

        return comment_data, 400

    logger.debug(
        f"Comentário de {user_data.get('userNickname')} adicionado com sucesso."
    )
    return result, 200


@forum_bp.delete("/comment/<comment_id>", responses={"200": RemoveCommentResponse})
def remove_comment(path: CommentPathSchema):
    user = session.get("user")
    if not user:
        logger.warning("Usuário não logado!")
        return {"error": "User not logged in!"}, 403

    user_info = user.get("userinfo")
    user_data = {
        "userEmail": user_info.get("email"),
        "userID": user_info.get("sub"),
        "userNickname": user_info.get("nickname"),
    }

    variables = {"commentID": path.comment_id}
    variables.update(user_data)

    logger.debug(f"Removendo comentário de usuário {user_data.get('userNickname')}")
    response = requests.post(
        url=forum_api_url,
        json={"query": remove_comment_mutation, "variables": variables},
    )
    comment_data = response.json()
    result = comment_data.get("data")
    if comment_data.get("errors") or result.get("removeComment").get("errors"):
        erro_msg = comment_data.get("errors") or result.get("removeComment").get(
            "errors"
        )
        logger.warning(f"Erro ao remover comentário: {erro_msg}")

        return comment_data, 400

    logger.debug(f"Comentário de {user_data.get('userNickname')} removido com sucesso.")
    return result, 200


@forum_bp.put("/comment/<comment_id>", responses={"200": UpdateCommentResponse})
def update_comment(path: CommentPathSchema, body: UpdateCommentBodySchema):
    user = session.get("user")
    if not user:
        logger.warning("Usuário não logado!")
        return {"error": "User not logged in!"}, 403

    user_info = user.get("userinfo")
    user_data = {
        "userEmail": user_info.get("email"),
        "userID": user_info.get("sub"),
        "userNickname": user_info.get("nickname"),
    }

    variables = {
        "commentID": path.comment_id,
        "content": body.content,
    }
    variables.update(user_data)

    logger.debug(f"Atualizando comentário de usuário {user_data.get('userNickname')}")
    response = requests.post(
        url=forum_api_url,
        json={"query": update_comment_mutation, "variables": variables},
    )
    comment_data = response.json()
    result = comment_data.get("data")
    if comment_data.get("errors") or result.get("updateComment").get("errors"):
        erro_msg = comment_data.get("errors") or result.get("updateComment").get(
            "errors"
        )
        logger.warning(f"Erro ao atualizar comentário: {erro_msg}")

        return comment_data, 400

    logger.debug(
        f"Comentário de {user_data.get('userNickname')} atualizado com sucesso."
    )
    return result, 200
