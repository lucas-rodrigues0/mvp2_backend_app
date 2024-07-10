from pydantic import BaseModel
from typing import Optional, List
import uuid
import datetime

from schemas.common_schemas import MessageSchema


class ArticlePathSchema(BaseModel):
    """Representação do paramêtro de path para artigo."""

    article_id: str


class AddArticleBodySchema(BaseModel):
    """Representação do corpo de requisição para adicionar artigo."""

    title: str
    content: str


class UpdateArticleBodySchema(BaseModel):
    """Representação do corpo de requisição para atualizar artigo."""

    title: Optional[str] = None
    content: Optional[str] = None


class ArticleCommentReplySchema(BaseModel):
    """Representação dos comentários relacionados a um artigo."""

    commentId: uuid.UUID
    userNickname: str
    content: str
    updatedAt: datetime.datetime


class ArticleCommentsSchema(ArticleCommentReplySchema):
    """Representação dos comentários relacionados a um artigo incluindo a lista
    de respostas desses comentários."""

    replies: Optional[List[ArticleCommentReplySchema]] = None


class ArticleBasicSchema(BaseModel):
    """Representação de um artigo base."""

    articleId: uuid.UUID
    userNickname: str
    title: str


class ArticleSchema(ArticleBasicSchema):
    """Representação de um artigo com a lista dos comentários que são relacionados."""

    content: str
    updatedAt: datetime.datetime
    comments: List[ArticleCommentsSchema]


class GetArticlesResponse(BaseModel):
    """Representação da resposta a requisição que busca lista de artigos."""

    articles: List[ArticleSchema]


class GetArticleByIdResponse(BaseModel):
    """Representação da resposta a requisição que busca um artigo por seu ID."""

    articleById: ArticleSchema


class GetArticleByUserResponse(BaseModel):
    """Representação da resposta a requisição que busca lista de artigos de usuário específico."""

    articleByUserId: List[ArticleSchema]


class GetArticleByPeriodResponse(BaseModel):
    """Representação da resposta a requisição que busca lista de artigos de um período específico."""

    articleByPeriod: List[ArticleSchema]


class AddArticleResponse(BaseModel):
    """Representação da resposta a requisição que insere novo artigo."""

    addArticle: ArticleBasicSchema


class RemoveArticleResponse(BaseModel):
    """Representação da resposta a requisição que remove artigo."""

    removeArticle: MessageSchema


class ArticleUpdate(ArticleBasicSchema):
    """Representação de um artigo atualizado."""

    content: str
    updatedAt: datetime.datetime


class UpdateArticleResponse(BaseModel):
    """Representação da resposta a requisição que atualiza artigo."""

    updateArticle: ArticleUpdate
