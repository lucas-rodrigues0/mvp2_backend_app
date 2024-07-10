from pydantic import BaseModel
from typing import List, Optional, Dict


class ByUserPathSchema(BaseModel):
    """Representação do paramêtro de path para ID de um usuário."""

    user_id: str


class ByPeriodQueryParamSchema(BaseModel):
    """Representação do paramêtro de query para as datas de inicio e fim de período."""

    initialDate: str
    endDate: str


class MessageSchema(BaseModel):
    """Representação padrão para mensagem em respostas."""

    message: str


class ErrorsInfo(BaseModel):
    """Representação para as informações de um erro da api graphql."""

    locations: List[Dict[str, int]]
    message: str
    path: Optional[List[str]]


class ErrorSchema(BaseModel):
    """Representação para a resposta contendo mensagem de erro."""

    data: None
    errors: List[ErrorsInfo]
