from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from loguru import logger

from common.api.responses import responses as HTTP_RESPONSES
from starlette.status import HTTP_301_MOVED_PERMANENTLY

################################################################################
### En app/model/rest.py se definen los modelos que servirán para comunicarse
### con el front end (tanto los que se reciben como los que se devuelven)
################################################################################
from model.serializers import ShortURLResponse, URLBase, URLCreate
from services import base_handler as handler

################################################################################
### Se pueden definir errores personalizados (ver la implementación en el
### archivo EntityNotFoundException)
################################################################################
router = APIRouter(responses=HTTP_RESPONSES)


################################################################################
### Se definen los parámetros que se reciben y los que se devuelven con base
### en el modelo
################################################################################
@router.post("/shorten", response_model=ShortURLResponse)
# Solo usar async def si se requiere hacer await
def shortener(url: URLCreate) -> ShortURLResponse:
    return handler.create_short_url(url=url)


@router.get("/{short_code}", response_model=URLBase)
# Solo usar async def si se requiere hacer await
def get_redirect_short_code(short_code: str) -> URLBase:
    return RedirectResponse(
        url=handler.get_original_url_by_short_code(short_code=short_code).original_url,
        status_code=HTTP_301_MOVED_PERMANENTLY,
    )
