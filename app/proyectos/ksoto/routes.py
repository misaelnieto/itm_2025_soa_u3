"""Uso de API ROUTES para manejo de peliculas en una API.

Routes:
    - GET     /getMovies:   Devuelve la lista de todas las peliculas
    - POST    /newMovie:    Inserta una nueva pelicula
    - PUT     /modifyMovie: Modifica uno o mas campos de una misma pelicula
    - DELETE  /deleteMovie: Elimina una pelicula por medio de un Identificador y del nombre

Functions:
    - devolverPeliculas:        Es el metodo que se encarga de devolver en la respuesta la lista de las peliculas
    - agregarNuevaPelicula:     Es el metodo que inserta una pelicula en base a los datos del cliente
    - ModificarDatosDePelicula: Es el metodo que modifica datos de una pelicula en particular
    - eliminarUnaPelicula:      Es el metodo que elimina una pelicula

Dependencias:
    - [fastapi](https://fastapi.tiangolo.com/): Framework FastAPI para construir APIs.
    - [pydantic](https://docs.pydantic.dev/): Validación de datos y gestión de configuraciones utilizando anotaciones de tipo de Python.
    - [sqlalchemy](https://www.sqlalchemy.org/): Toolkit SQL y librería de Mapeo Objeto-Relacional (ORM).
    - [sqlmodel](https://sqlmodel.tiangolo.com/): Bases de datos SQL en Python, diseñado para ser compatible con FastAPI.
    - `app.main`: Módulo principal de la aplicación que contiene la sesión de base de datos.
    - `.models`: Módulo que contiene el modelo de Películas.
    - `.schemas`: Módulo que contiene los esquemas de respuesta (`ConfirmResponse`, `RequestType`, `ReturnMovie`, `changeDataBodyJSON`, `identifyMovie`).
"""

from fastapi import APIRouter
from sqlmodel import select

from app.db import DbSession
from app.proyectos.ksoto.schemas import (
    ConfirmResponse,
    RequestType,
    ReturnMovie,
    StatusType,
    changeDataBodyJSON,
    identifyMovie,
)

from .models import Peliculas

api_router = APIRouter(
    prefix="/pelicula",
    tags=["Peliculas"],
    responses={404: {"description": "Not found"}},
)





@api_router.get("/movie/{id_movie}/{name}", tags=["Pelicula"])
def devolverPelicula(id_movie:int, name:str, db:DbSession) -> ConfirmResponse:
    """Metodo para buscar y encontrar una pelicula en particular."""
    movie = db.exec(select(Peliculas).where(Peliculas.id == id_movie and Peliculas.name == name)).first()

    if movie is None:
        recibido = identifyMovie(id=id_movie,name=name)
        return ConfirmResponse(type='GET', status=StatusType.fail, comment=f"There's no movie with the id:{id_movie} and with the name:{name}", returnJson=recibido)


    cleanPelicula = ReturnMovie(name=movie.name, director=movie.director, release=movie.release)
    return ConfirmResponse(type='GET', status=StatusType.succes, comment='Here is your movie', returnJson=cleanPelicula)






@api_router.get("/movies", tags=["Pelicula"])
def devolverPeliculas(db: DbSession) -> ConfirmResponse:
    """Metodo para devolver todas las peliculas."""
    listPeliculas =  db.exec(select(Peliculas)).all()

    listRP = []

    # crear un arreglo de tipo ReturnMovie, el cual es mucho mas limpio
    for pelicula in listPeliculas:
        listRP.append(ReturnMovie(name=pelicula.name,  director=pelicula.director,  release=pelicula.release))
    
    return ConfirmResponse(type=RequestType.get,status=StatusType.succes, comment="Here the list of all data your requested",  returnJson=listRP)
    





@api_router.post("/movies", tags=["Pelicula"])
def agregarNuevaPelicula(db:DbSession, request: ReturnMovie) -> ConfirmResponse:
    """Metodo para recibir una pelicula y agregarla a la base de datos."""
    new_movie = Peliculas(name=request.name,director=request.director,release=request.release)
    peliculaLimpia = ReturnMovie(name=new_movie.name, director=new_movie.director, release = new_movie.release)

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    
    return ConfirmResponse(type=RequestType.post, status=StatusType.succes, comment="Here the list of all data your requested", returnJson=peliculaLimpia)
    
    






@api_router.put("/movies", tags=["Pelicula"])
def ModificarDatosDePelicula(db:DbSession, request: changeDataBodyJSON) -> ConfirmResponse:
    """Metodo para modificar un dato de la pelicula."""
    # Seleccionar si el id coincide con el de alguna pelicula

    movie = db.exec(select(Peliculas).where(Peliculas.id == request.identificador.id and Peliculas.name == request.identificador.name)).first()

    if movie is None:
        return ConfirmResponse(type=RequestType.put, status=StatusType.fail, comment=f"The movie with the id:{request.identificador.id} and with the name:{request.identificador.name} does not exist!!",returnJson=request)

    # Significa que la pelicula si existe

    if request.new_name is not None:
        movie.name = request.new_name

    if request.new_director is not None:
        movie.director = request.new_director

    if request.new_release is not None:
        movie.release = request.new_release


    
    db.commit()
    db.refresh(movie)
    

    peliculaLimpia = ReturnMovie(name=movie.name,director=movie.director,release=movie.release)
    return ConfirmResponse(type=RequestType.put, status=StatusType.succes, comment="The data was modified successfully",returnJson=peliculaLimpia)







@api_router.delete("/movies/{id_pelicula}/{name}", tags=["Pelicula"])
def eliminarUnaPelicula(id_pelicula:int, name:str, db: DbSession) -> ConfirmResponse:  # noqa: A002
    """Metodo para eliminar una pelicula."""
    # Comment


    # Crear un request
    request = identifyMovie(id=id_pelicula,name=name)

    movie = db.exec(select(Peliculas).where(Peliculas.id == id_pelicula and Peliculas.name == name)).first()
   
    if movie is None:
        return ConfirmResponse(type=RequestType.delete, status=StatusType.fail, comment=f"The movie with the id:{id_pelicula} and with the name:{name} doesn't exist!!",returnJson=request)
    
    
    db.delete(movie)
    db.commit()
    
    return ConfirmResponse(type=RequestType.delete, status=StatusType.succes, comment="The removal was successful!!", returnJson=request)

    
