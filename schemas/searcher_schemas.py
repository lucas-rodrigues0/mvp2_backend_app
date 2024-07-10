from pydantic import BaseModel


class QuerySchema(BaseModel):
    """Representação do paramêtro de query para os termos utilizados na pesquisa
    de texto completo do serviço Searcher API."""

    term: str


class PageInfoSchema(BaseModel):
    """Representação das informações de página de um resultado da pesquisa."""

    Título: str
    Capítulo: str


class PageSchema(BaseModel):
    """Representação de página contendo um dos resultados da pesquisa."""

    page_info: PageInfoSchema
    content: str


class PageNumSchema(BaseModel):
    """Representação do retorno de um resultado da pesquisa."""

    page_num: PageSchema


class SearcherResponse(BaseModel):
    """Representação da resposta com todos os resultados da pesquisa."""

    results: PageNumSchema
