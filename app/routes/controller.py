import os
import time

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from loguru import logger
from pydantic import errors
from pydantic.error_wrappers import ValidationError
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from common.api.responses import responses as HTTP_RESPONSES
from model.errors import EntityNotFoundException, NotFoundMessage

################################################################################
### En app/model/rest.py se definen los modelos que servirán para comunicarse
### con el front end (tanto los que se reciben como los que se devuelven)
################################################################################
from model.serializers import ShortURLResponse, URLCreate
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
    pass
    
    

