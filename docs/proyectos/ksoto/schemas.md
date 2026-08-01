# Esquemas


En el archivo ksoto/schemas.py tenemos en clases los moldes o formatos de como queremos ya sea recibir o devolver un json.



Las clases que heredan BaseModel definen como dijimos al principio, la forma en la que queremos recibir o enviar un JSON en particular, por ejemplo:

    class ReturnMovie(BaseModel):

        name : str
        director : str
        release : str

En este metodo que implementa BaseModel, estamos diciendo que cuando una metodo en routes reciba un JSON de tipo ReturnMovie, el formato de ese JSON deberia ser el siguiente:

  {
    name:"Some Movie",
    director:"Cristiano Ronaldo",
    release:"2011-10-05T14:48:00.000Z"
  }

Es decir, si el cliente le envia a un metodo que recibe un ReturnMovie un JSON diferente, la API no lo reconocera, por ejemplo, un JSON como el siguiente:

  {
    nameMovie:"Some Movie",
    release:"2011-10-05T14:48:00.000Z"
    director:"Cristiano Ronaldo",
  }



## JSON que regresara la API al cliente


Todos los metodos en el archivo ksoto/routes.py retornar un json de tipo ConfirmResponse(), el cual es el siguiente:

    class ConfirmResponse(BaseModel):

    type: RequestType
    status: StatusType
    comment: str
    returnJson: list[ReturnMovie] | ReturnMovie | changeDataBodyJSON | identifyMovie | None


A continuacion, explicaremos que significa cada campo de los 4 que podemos encontrar en la clase:

type se refiere al metodo de la solicitud que recibio la API, es decir, si un cliente, usuario u otro servidor le manda a la API una solicitud de tipo PUT, la API va a capturar ese valor, y cuando devuelva el resultado, pondra en type "PUT". 

status es una clase StrEnum que solo puede contener dos valores "success" o "fail", por ejemplo, si la operacion que nosotros queriamos ejecutar es eliminar un usuario, y efectivamente se hizo la eliminacion, en la respuesta de la API, veremos en el campo status el string "success"; sin embargo; si por alguna razon no se hizo la eliminacion, ya sea un error de la base de datos, un error de la misma API, algun parametro mal configurado, etc, nos escribira en status el string "fail".

comment es para darnos mas contexto de que fue lo que paso, es decir, si hubo un error, si algo salio mal, nos dara el mensaje de que lo que paso tal cual.

returnJson es el campo en el que almacenaremos la verdadera respuesta que queremos darle al cliente, por ejemplo, si queremos devolver una lista de Peliculas, esa lista deberia de ir en returnJson. En algunos casos returnJson podria ser de tipo None, por ejemplo, si el usuario elimina una Pelicula, y esa eliminacion fue exitosa, el status seria "success", el comment seria algo como "The user was deleted successfully", mientras que el returnJson no hay necesidad de enviar el json de la Pelicula en cuestion, es decir, de una pelicula que ya no existe.