from pydantic import BaseModel
from typing import Optional, List
import uuid
import datetime

from schemas.common_schemas import MessageSchema


class CommentPathSchema(BaseModel):
    comment_id: str


class AddCommentBodySchema(BaseModel):
    article_id: str
    content: str
    is_reply: Optional[bool] = None
    comment_reply: Optional[str] = None


class UpdateCommentBodySchema(BaseModel):
    content: str


class ReplySchema(BaseModel):
    commentId: uuid.UUID
    commentReply: Optional[uuid.UUID] = None
    content: str
    isReply: bool
    userNickname: str


class CommentSchema(ReplySchema):
    articleId: uuid.UUID


class CommentWithDateSchema(CommentSchema):
    updatedAt: datetime.datetime


class CommentRepliesSchema(CommentWithDateSchema):
    replies: Optional[List[ReplySchema]] = None


class GetCommentsResponse(BaseModel):
    comments: List[CommentRepliesSchema]


class GetCommentByIdResponse(BaseModel):
    commentById: CommentWithDateSchema


class GetCommentByUserIdResponse(BaseModel):
    commentByUserId: List[CommentWithDateSchema]


class GetCommentByPeriodResponse(BaseModel):
    commentByPeriod: List[CommentRepliesSchema]


class AddCommentResponse(BaseModel):
    addComment: CommentSchema


class RemoveCommentResponse(BaseModel):
    removeComment: MessageSchema


class UpdateCommentResponse(BaseModel):
    updateComment: CommentSchema
