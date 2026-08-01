"""Esquemas de validacion."""
from enum import StrEnum

from pydantic import BaseModel


class RequestType(StrEnum):
    """Solo hay 4 posibles transacciones."""

    get = "GET"
    post = "POST"
    delete = "DELETE"
    put = "PUT"


class StatusType(StrEnum):
    """Tipos de status que se pueden dar."""

    succes = "success"
    fail = "fail"




# Retornar una o mas peliculas GET
class ReturnMovie(BaseModel):
    """Definar lo que quiero devolver o recibir cuando un usuario me pida una sola pelicula."""

    name : str
    director : str
    release : str





class identifyMovie(BaseModel):
    """Formato JSON con los datos minimos para identificar apropiadamente una pelicula."""

    id : int
    name : str


class changeDataBodyJSON(BaseModel):
    """"Cuerpo del JSON para recibir una peticion de tipo 'modificar datos de una pelicula'."""

    identificador: identifyMovie
    new_name : str | None
    new_director : str | None
    new_release : str | None


# Respuesta standard
class ConfirmResponse(BaseModel):
    """Este es el cuerpo del json para validar un transaccion."""

    type: RequestType
    status: StatusType
    comment: str
    returnJson: list[ReturnMovie] | ReturnMovie | changeDataBodyJSON | identifyMovie | None
