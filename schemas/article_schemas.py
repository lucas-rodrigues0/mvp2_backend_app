from pydantic import BaseModel
from typing import Optional, List
import uuid
import datetime

from schemas.common_schemas import MessageSchema


class ArticlePathSchema(BaseModel):
    article_id: str


class AddArticleBodySchema(BaseModel):
    title: str
    content: str


class UpdateArticleBodySchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class ArticleCommentReplySchema(BaseModel):
    commentId: uuid.UUID
    userNickname: str
    content: str
    updatedAt: datetime.datetime


class ArticleCommentsSchema(ArticleCommentReplySchema):
    replies: Optional[List[ArticleCommentReplySchema]] = None


class ArticleBasicSchema(BaseModel):
    articleId: uuid.UUID
    userNickname: str
    title: str


class ArticleSchema(ArticleBasicSchema):
    content: str
    updatedAt: datetime.datetime
    comments: List[ArticleCommentsSchema]


class GetArticlesResponse(BaseModel):
    articles: List[ArticleSchema]


class GetArticleByIdResponse(BaseModel):
    articleById: ArticleSchema


class GetArticleByUserResponse(BaseModel):
    articleByUserId: List[ArticleSchema]


class GetArticleByPeriodResponse(BaseModel):
    articleByPeriod: List[ArticleSchema]


class AddArticleResponse(BaseModel):
    addArticle: ArticleBasicSchema


class RemoveArticleResponse(BaseModel):
    removeArticle: MessageSchema


class ArticleUpdate(ArticleBasicSchema):
    content: str
    updatedAt: datetime.datetime


class UpdateArticleResponse(BaseModel):
    updateArticle: ArticleUpdate
