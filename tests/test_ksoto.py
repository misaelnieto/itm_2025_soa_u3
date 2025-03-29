"""# 🧪 Test de la API peliculas.

Este modulo contiene test para la API peliculas. Verifica lo siguiente:
 - Que los datos se reciban bien entre funciones
 - Que las funciones efectivamente funcionen como debe de ser
 - Que retornar el formato esperado a lo establecido en el modulo schemas
"""
from datetime import datetime

from app.proyectos.ksoto.schemas import ConfirmResponse, ReturnMovie, changeDataBodyJSON, identifyMovie

BASE_PATH = "/api/v1/ksoto/pelicula/movies"



def test_obtenerPeliculas(rest_api):
    """Metodo en el que se hacen las pruebas del metodo 'devolverPeliculas'."""
    # Agregar una pelicula para no obtener una lista vacia
    first_movie = ReturnMovie(name="Spiderman",director="Sam Raimi", release=datetime(2002,5,3).isoformat())

    rest_api.post(
        f"{BASE_PATH}",
        json=first_movie.dict(),
    )


    response = rest_api.get(
        f"{BASE_PATH}",
    )

    r = ConfirmResponse(**response.json())
    assert r.returnJson[0].name == 'Spiderman'
    assert r.returnJson[0].release == datetime(2002,5,3).isoformat()



def test_obtenerPelicula(rest_api):
    """Metodo en el que se hacen las pruebas del metodo 'devolverPelicula'."""
    # Agregar una pelicula para poder buscarla y devolverla
    first_movie = ReturnMovie(name="Titanic",director="James Cameron", release=datetime(1998,1,1).isoformat())

    rest_api.post(
        f"{BASE_PATH}",
        json=first_movie.dict(),
    )



    # Ahora toca buscar la pelicula
    id_m = 1
    name_m = 'Titanic'

    response = rest_api.get(
        f"/api/v1/ksoto/pelicula/movie/{id_m}/{name_m}",
    )

    ConfR = ConfirmResponse(**response.json())

    Pelicula = ConfR.returnJson

    assert Pelicula.director == 'James Cameron'
    assert Pelicula.release == datetime(1998,1,1).isoformat()




    # Buscar una pelicula que no existe
    response = rest_api.get(
        "/api/v1/ksoto/pelicula/movie/2/Megamind",
    )

    ConfR = ConfirmResponse(**response.json())

    # Se espera nos envia solo lo que le enviamos
    assert ConfR.comment == "There's no movie with the id:2 and with the name:Megamind"





def test_agregarPelicula(rest_api):
    """Metodo en el que se hacen las pruebas del metodo que agrega peliculas."""
    first_movie = ReturnMovie(name="Titanic",director="James Cameron", release=datetime(1998,1,1).isoformat())

    first_response = rest_api.post(
        f"{BASE_PATH}",
        json=first_movie.dict(),
    )

    ConR1 = ConfirmResponse(**first_response.json())
    
    Pelicula1 = ConR1.returnJson

    assert Pelicula1.name == 'Titanic'
    assert Pelicula1.director == 'James Cameron'
    assert Pelicula1.release == datetime(1998,1,1).isoformat()









def test_modificarDatos(rest_api):
    """Metodo para hacer pruebas del metodo 'ModificarDatosDePelicula'."""
    # Agregar una Pelicula en este metodo para poder modificar

    first_movie = ReturnMovie(name="jurasik Park",director="Messi", release=datetime(2018,2,24).isoformat())

    rest_api.post(
        f"{BASE_PATH}",
        json=first_movie.dict(),
    )

    identificador = identifyMovie(id=1,name="jurasik Park")
    modificarMovie = changeDataBodyJSON(identificador=identificador,new_name="Jurassic Park",new_director="Steven Spielberg",new_release=datetime(1993,6,9).isoformat())
    

    response = rest_api.put(
        f"{BASE_PATH}",
        json=modificarMovie.dict(),
    )


    JSON_recibido = ConfirmResponse(**response.json())

    
    PeliculaModificada = JSON_recibido.returnJson

    assert PeliculaModificada.director == "Steven Spielberg"
    assert PeliculaModificada.name == "Jurassic Park"



    # Ahora vamos a modificar una pelicula que no existe
    identificador2 = identifyMovie(id=4,name="Toy Stories")
    modificarMovie2 = changeDataBodyJSON(identificador=identificador2,new_name="Toy Story",new_director="John Lasseter",new_release=datetime(1995,11,22).isoformat())


    response2 = rest_api.put(
        f"{BASE_PATH}",
        json=modificarMovie2.dict(),
    )

    JSON_recibido2 = ConfirmResponse(**response2.json())


    assert JSON_recibido2.comment == "The movie with the id:4 and with the name:Toy Stories does not exist!!"
    assert JSON_recibido2.returnJson == modificarMovie2



def test_eliminarDatos(rest_api):
    """Metodo para hacer pruebas del metodo 'eliminarUnaPelicula'."""
    # Agregar una Pelicula en este metodo para poder eliminar

    first_movie = ReturnMovie(name="Back to the Future",director="Robert Zemeckis", release=datetime(1985,7,3).isoformat())
    rest_api.post(
        f"{BASE_PATH}",
        json=first_movie.dict(),
    )



    # Ahora vamos a eliminar una pelicula que no existe

    test_id = 8
    test_nombre = "Cars"

    test_response = rest_api.delete(
        f"{BASE_PATH}/{test_id}/{test_nombre}",
    )

    test_ConR = ConfirmResponse(**test_response.json())

    assert test_ConR.comment == "The movie with the id:8 and with the name:Cars doesn't exist!!"
    assert test_ConR.returnJson == identifyMovie(id=test_id,name=test_nombre)




    
    # Ahora vamos a eliminar una pelicula que si existe

    id_pelicula = 1
    nombre = "Back to the Future"

    response = rest_api.delete(
        f"{BASE_PATH}/{id_pelicula}/{nombre}",
    )

    ConR = ConfirmResponse(**response.json())

    assert ConR.comment == "The removal was successful!!"
    assert ConR.returnJson == identifyMovie(id=id_pelicula,name=nombre)

