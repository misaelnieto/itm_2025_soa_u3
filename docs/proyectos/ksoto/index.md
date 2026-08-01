# API Peliculas 


La API Peliculas es una API que fue desarrollo en python usando la tecnologia fastAPI. Es una API que te permite gestionar peliculas sin necesidad de tener una base de datos, ya que la misma API tiene su propia base de datos en donde se guardan las peliculas que distintos usuarios han ido agregando.



## Estructura de la API

La api esta estructurada principalmente en 3 archivos: models.py, schemas.py y routes.py, siendo routes.py quien se encarga de manejar la logica de la API; es decir, de definir los metodos que se van a ejecutar cuando se reciba una ruta y un metodo HTTP en especifico. 

El archivo models.py es el que define las tablas que se van usar, asi como los campos que hay en ellas. Es decir, si un campo almacenara texto o algun dato numerico, si ese campo permite valores null o no, etc. 

El archivo schemas.py por otro lado, define la forma en la que se quiere recibir un JSON en especifico, o enviar dicho JSON. Es decir, contiene clases que definen el molde que deben de llevar todos los JSON del tipo de la clase.






## Uso de la API

Muy probablemente las palabras no sean suficientes para explicar como se debe usar la API desde el cliente, recordando que el cliente en su mayoria sera otro servidor que utilice la API para realizar algun procedimiento, obtener una Pelicula en particular, sin tener que ese servidor tenga que implementar su propia logica.


A continuacion, mostraremos como usar cada uno de los metodos que la API puede ejecutar tomando como ejemplo un servidor de nodeJS:





### Agregar Pelicula

La api contiene un metodo llamado <b>agregarNuevaPelicula()</b>, este metodo lo que hace es recibir todos los campos minimos para poder crear una nueva pelicula. A continuacion mostraremos como usarlo con nodeJS:
       
    let response = await fetch("http://localhost:8000/api/v1/ksoto/pelicula/movies",{
        method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify({
            name:name,
            director:director,
            release:releaseISO
        })
    });

En este caso, las variables name, director, y releaseISO son cadenas de texto, si llegaramos a enviarle datos de otro tipo, como un enteros, nos daria error





### Eliminar Pelicula

La API utiliza el metodo <b>eliminarUnaPelicula()</b>, este metodo recibe como parametros de ruta el id y el nombre de una pelicula en particular. Recordemos que por defecto, en fastAPI el metodo HTTP DELETE no recibe un body, es por esta razon que no podemos pasar el id y el nombre en el body, es decir, tenemos que pasarlos como parametros de ruta. A continuacion un ejemplo de uso con nodeJS:

  let response = await fetch(`http://localhost:8000/api/v1/ksoto/pelicula/movies/${id}/${name}`,{
        method:'DELETE',
        headers:{
            'Content-Type':'application/json'
        }
  });

En el ejemplo, podemos ver claramente como el id y el name se lo estamos enviando como parametros GET, aunque el metodo sea DELETE, esto es completamente valido.



### Modificar Datos de una Pelicula

En la API tenemos el metodo <b>ModificarDatosDePelicula()</b>, este metodo es como su mismo nombre lo indica, para modificar datos de una pelicula en particular. Puede ser que hayamos registrado una pelicula, pero nos equivocamos en la fecha, asi que logicamente vamos a querer corregir ese campo mal ingresado. Este metodo recibe un JSON con 4 parametros: 
  -id: Para identificar la pelicula a la que queremos acceder
  -name: Contiene el nombre, y se usa junto con el ID para buscar la pelicula que se quiere modificar
  -new_name: Puede ser null (None) o bien un string
  -new_director: Puede ser null (None) o bien un string
  -new_release: Puede ser null (None) o bien un string

Solo los primeros dos campos son obligatorios, los otros no lo son. La API detectara cuales son nulos y cuales no, y solo cambiara los datos que no sean nulos. Cabe mencionar que id y name en realidad no son hijos director del JSON, es decir, la estructura del JSON seria realmente algo como lo siguiente:


   {
        identificador: {
            id:10,
            name:"some name"
        },
        new_name:"Transformers",
        new_director:"Juan",
        new_release:null
   }



Acontinuacion, mostraremos como comunicarnos con este metodo desde un servidor utilizando nodeJS:

        let response = await fetch("http://localhost:8000/api/v1/ksoto/pelicula/movies",{
            method:'PUT',
            headers:{
                'Content-Type':'application/json'
            },
            body:{
                identificador:{
                    id:id,
                    name:name,
                },
                new_name:new_name,
                new_director:new_director,
                new_release:fechaISO
            }
        });

    


### Obtener una Lista de Todas las Peliculas


La API en routes.py tiene el metodo <b>devolverPeliculas()</b>, el cual se encarga de devolver una lista de todas las Peliculas almacenadas en la Base de Datos de la API, este metodo es de tipo get, y no necesita recibir ningun parametro de ruta, y logicamente al ser de tipo get tampoco recibe paramtros en el body, debido a que el metodo HTTP GET no tiene un body, a continuacion un caso de uso:

    let response = await fetch('http://localhost:8000/api/v1/ksoto/pelicula/movies',{
        method:'GET',
        headers:{
            'Content-Type':'application/json'
        }
    });



### Obtener una Pelicula en particular

Aveces lo que queremos no es una lista que contenga un monton de peliculas, sino obtener una Pelicula en especifico para hacer una operacion con la misma. La API maneja un metodo que tiene como nombre <b>devolverPelicula()</b>, este metodo recibe el id y el name de la Pelicula para poder buscar dicha Pelicula.

Al ser un metodo HTTP GET, recibe tanto el id y el name dentro de la ruta, sin embargo, no llegue a pensar que el id y el name estan dentro de un JSON, y que posteriormente se pone ese JSON en la ruta. Recordemos que FastAPI por defecto no puede aceptar JSON en la misma ruta, es decir, lo siguiente es TOTALMENTE INCORRECTO:
   
    let JSON = {
        id:32,
        name:'Avatar'
    };

    let response = await fetch(`http://localhost:8000/api/v1/ksoto/pelicula/movie/${JSON}`,{
            method:'GET',
            headers:{
                'Content-Type':'application/json'
            }
    });


FastAPI solo acepta campos normales en las rutas, es decir, campos de tipo int, de tipo str, de tipo None (null en otros lenguajes), etc.


La manera de usar este metodo es el siguiente:

        let response = await fetch(`http://localhost:8000/api/v1/ksoto/pelicula/movie/${id_movie}/${name}`,{
            method:'GET',
            headers:{
                'Content-Type':'application/json'
            }
        });