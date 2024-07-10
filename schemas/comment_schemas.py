from pydantic import BaseModel
from typing import Optional, List
import uuid
import datetime

from schemas.common_schemas import MessageSchema


class CommentPathSchema(BaseModel):
    """Representação do paramêtro de path para comentário."""

    comment_id: str


class AddCommentBodySchema(BaseModel):
    """Representação do corpo de requisição para adicionar comentário."""

    article_id: str
    content: str
    is_reply: Optional[bool] = None
    comment_reply: Optional[str] = None


class UpdateCommentBodySchema(BaseModel):
    """Representação do corpo de requisição para atualizar comentário."""

    content: str


class ReplySchema(BaseModel):
    """Representação de um comentário sendo ele uma resposta a outro comentário ou não."""

    commentId: uuid.UUID
    commentReply: Optional[uuid.UUID] = None
    content: str
    isReply: bool
    userNickname: str


class CommentSchema(ReplySchema):
    """Representação de um comentário com o ID do artigo a qual se relaciona."""

    articleId: uuid.UUID


class CommentWithDateSchema(CommentSchema):
    """Representação de um comentário com a data da última atualização."""

    updatedAt: datetime.datetime


class CommentRepliesSchema(CommentWithDateSchema):
    """Representação de comentário com as respostas feitas a esse comentário"""

    replies: Optional[List[ReplySchema]] = None


class GetCommentsResponse(BaseModel):
    """Representação da resposta a requisição que busca lista de comentários."""

    comments: List[CommentRepliesSchema]


class GetCommentByIdResponse(BaseModel):
    """Representação da resposta a requisição que busca um comentário por seu ID."""

    commentById: CommentWithDateSchema


class GetCommentByUserIdResponse(BaseModel):
    """Representação da resposta a requisição que busca lista de comentários de usuário específico."""

    commentByUserId: List[CommentWithDateSchema]


class GetCommentByPeriodResponse(BaseModel):
    """Representação da resposta a requisição que busca lista de comentários de um período específico."""

    commentByPeriod: List[CommentRepliesSchema]


class AddCommentResponse(BaseModel):
    """Representação da resposta a requisição que insere novo comentário."""

    addComment: CommentSchema


class RemoveCommentResponse(BaseModel):
    """Representação da resposta a requisição que remove comentário."""

    removeComment: MessageSchema


class UpdateCommentResponse(BaseModel):
    """Representação da resposta a requisição que atualiza comentário."""

    updateComment: CommentSchema
