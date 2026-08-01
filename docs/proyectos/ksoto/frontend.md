#  Servidor que se conecta con la API Peliculas de fastAPI


## Creacion de proyecto e instalaciones de dependencias

El servidor que se conecta con la API Peliculas fue hecho con nodejs, usando el framework express, un framework que nos permite levantar servidores con nodejs.

Antes que nada, debemos tenemos que crear un proyecto de nodejs, para hacer esto primero ejecutamos el comando: npm init -y

Posteriormente debemos de instalar las dependencias que necesitaremos, en este caso, necesitaremos instalar express, el comando para instalarlo es el siguiente: npm i express


## Configuracion del archivo package.json

Si necesitas hacer una configuracion, lo debes de hacer aqui, por ejemplo, en mi caso no me gustan la manera en que se hacen las importantes en nodejs con palabras claves como 'require'. En lo personal prefiero importaciones como las siguientes:

    import express from 'express';
    import path from 'path';


Por defecto, nodejs no soporta este tipo de importaciones, para que si lo haga debemos meternos al archivo package.json y poner la siguiente linea:

    "type": "module"



## Configuracion del servidor

La configuracion del servidor normalmente se hace en un archivo llamado index o main, en mi caso, es el archivo index, que se encuentra dentro de la carpeta app. Aqui importamos express, creamos una variable de llamada app y vamos a instanciar express en ella.


app debe tener todas las configuraciones correspondientes al servidor, por ejemplo, si queremos que nuestro servidor use express.json(), debemos hacercelo a la variable app. En codigo es asi:

   app.use(express.json());


Posteriormente en hay un metodo que es listen, en este metodo debemos definir el puerto en el que queremos que se levante nuestro servidor.


Las rutas se deben de hacer de la siguiente manera:

    app.get('/operaciones/obtenerPeliculas',operaciones.obtenerPeliculas);
    app.post('/operaciones/agregarPelicula',operaciones.agregarPelicula);
    app.delete('/operaciones/eliminarPelicula',operaciones.eliminarPelicula);


Lo que estamos haciendo es decirle al servidor que cuando reciba su dominio+ruta que podemos ver en cada uno, va a ejecutar algo, en este caso, metodos que estan en operaciones, que en nuestro caso es una objeto que contiene muchas funciones de un archivo que tenemos en nuestro archivo controllers.




## Organizacion del proyecto

Dentro de la carpeta app, tenemos todos los archivos js relacionados con el backend de nuestro servidor que en este caso el servidor entero es un frontend o un cliente que utilizara la api que hicimos con fastAPI.

Tambien tenemos una carpeta static, que contiene todo el frontend de nuestro servidor, es decir, tanto hojas de estilo, archivos HTML y scripts de JavaScript para controlar el DOM (Para fines de diseno)

Tenemos tambien el archivo  package.json, en donde tenemos las configuraciones necesarias