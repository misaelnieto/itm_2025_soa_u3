# Modelos de base de datos



En el archivo ksoto/models.py tenemos una modelo el cual es el siguiente:


    class Peliculas(SQLModel, table=True):

        __tablename__ = "tabla peliculas"
        id: int | None = Field(default=None, primary_key=True)
        name: str = Field(title="nombre", nullable=False)
        director: str = Field(title="director", nullable=False)
        release: str = Field(title="fecha de lanzamiento", nullable=False)


Cuando una clase en fastAPI implementa SQLModel, se entiende que esta clase sera tomada para contruir una tabla con las especificaciones correspondientes en la base de datos. Es decir, cuando arranquemos el backend, estas tablas van a ser creadas siempre y cuando no existan.

Esto nos da a entender que si apagamos el servidor y luego volvemos a arranquer el mismo, fastAPI no tratara de crear otra vez la tabla, sin embargo, si detecta cambios, como el haber agregado un campo nueva a la tabla, entonces hara las modificaciones necesarias, siempre y cuando las configuraciones que hayamos hecho sean correctas o no entren en conflicto con las anteriores.

Como podemos ver, nosotros tenemos 4 campos:

    id -> Representa el id de cada Pelicula, este id se lo podemos pasar directamente, pero si no se lo pasamos, le asignara None, cuando suceda esto la base de datos al detectar que se trata de la llave primaria, le asignara un id que es de tipo incremental.
    name -> Representa el nombre de la Pelicula, de tipo string y no debe ser null.
    director -> Representa el nombre del director de la Pelicula.
    release -> Es un string en donde nosotros vamos a almacenar la fecha, la razon de que sea de tipo string y no de tipo date es para no tener problemas con la diferencia de formatos de tipo datetime en diferentes tecnologias, por ejemplo, en nodejs, una fecha de tipo ISO es un poco diferente de una fecha en fastAPI de tipo ISO.


