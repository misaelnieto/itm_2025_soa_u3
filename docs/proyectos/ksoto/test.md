# Pruebas


En las pruebas tenemos el archivo test_ksoto.py, este archivo que se encuentra ubicado en la carpeta tests contiene las pruebas necesarias para la API de Peliculas, a continuacion explicaremos que hace el codigo.



## test_obtenerPeliculas

    def test_obtenerPeliculas(rest_api):
        
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



El metodo test_obtenerPeliculas ejecuta las pruebas que necesarias del metodo devolverPeliculas() del archivo ksoto/routes.py, Lo unico que hacemos es agregar una pelicula, y verificamos que en la respuesta nos haya enviado la data de la pelicula que fue creada, que en teoria debe ser la misma que la que le pasamos.


## test_obtenerPelicula

    def test_obtenerPelicula(rest_api):
    
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



En este metodo hacemos las pruebas del metodo devolverPelicula(), a diferencia del metodo devolverPeliculas() que nos retorna todas las listas, el metodo devolverPelicula() nos retorna solo la Pelicula que queremos encontrar, es decir, una pelicula en particular. Cabe mencionar que si agregamos un usuario en algun otro metodo del archivo test, este no se vera reflejado, es decir, que en el test para verificar el metodo que elimina peliculas, tambien tendremos que agregar una pelicula para poder eliminar una, de lo contrario, no podremos eliminar una porque las peliculas que hayamos agregado se perderan, esto sucede asi por la misma configuracion de las pruebas.




## test_agregarPelicula


    def test_agregarPelicula(rest_api):

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


Este metodo hace las pruebas del metodo en ksoto/routes.py agregarNuevaPelicula(), que como dijimos antes, en casi todos los metodos del archivo test hacemos insercion de Peliculas para hacer las pruebas correspondientes.



## test_modificarDatos

    def test_modificarDatos(rest_api):
        
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


Este metodo hace prubeas del metodo ModificarDatosDePelicula() ubicado en ksoto/routes.py, aqui se hacen las pruebas para verificar si la modificacion de Peliculas funciona. A continuacion explicare los pasos que hicimos:

1 - Agregar un Pelicula: Para modificar los datos de una pelicula, primero debemos tener peliculas existentes.
2 - Modificar la Pelicula: Como se puede apreciar en el codigo, agregamos una pelicula con datos erroneos a proposito, como el nombre del director, entonces para hacer la modificacion mandamos a llamar al metodo ModificarDatosDePelicula(), que recibe en el body un JSON de tipo changeDataBodyJSON(), ahi tenemos que poner los datos correspondientes para que nuestra funcion en routes.py puede trabajar.
3 - Hacemos la validaciones necesarias, es decir, comprobamos si la modificacion fue exitosa.
4 - Modificar una Pelicula que no existe: Luego volvemos a intener modificar una pelicula, pero que no existe, por lo que en el JSON de tipo changeDataBodyJSON() le pasamos un id y un name erroneo, es decir, buscara una pelicula con esos datos que le pasamos, pero no encontrara dicha pelicula.
5 - Posteriormente volvemos a hacer validaciones, como validar que efectivamente no se realizo ningun cambio.




## test_eliminarDatos

    def test_eliminarDatos(rest_api):
        
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


Aqui hacemos las pruebas del metodo eliminarUnaPelicula() que se encuentra en ksoto/routes.py, es decir, verificamos que la eliminacion de Peliculas en la API cumpla con las expectativas. Como podemos ver, hacemos pruebas para eliminar una Pelicula que si existe, y tambien hacemos para eliminar una Pelicula que no existe.