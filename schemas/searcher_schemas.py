from pydantic import BaseModel


class QuerySchema(BaseModel):
    term: str


class PageInfoSchema(BaseModel):
    Título: str
    Capítulo: str


class PageSchema(BaseModel):
    page_info: PageInfoSchema
    content: str


class PageNumSchema(BaseModel):
    page_num: PageSchema


class SearcherResponse(BaseModel):
    results: PageNumSchema
