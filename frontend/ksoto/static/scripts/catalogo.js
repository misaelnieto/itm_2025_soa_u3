let display = document.getElementsByClassName('fillData')[0];
let contenidoFDA = document.getElementsByClassName('contenidoFDA')[0];
let contenedor = document.getElementsByClassName('contenedorPeliculas')[0];


// Ejecutar esta funcion desde un principio
pedirTodasLasPeliculas();


async function pedirTodasLasPeliculas(){

    let response = await fetch("http://localhost:5010/operaciones/obtenerPeliculas",{
        method:'GET',
        headers:{
            'Content-Type':'application/json'
        }
    });

    if(!response.ok){

        console.log('No se pudo comunicar con el backend');

    }else{

        let responseJson = await response.json();
        

        if(responseJson.error){
            // Significa que hubo un error, toca levantar un alert

            display.style.display = "inline-block";
            contenidoFDA.textContent = responseJson.error;

            setTimeout(()=>{
                display.style.display = "none";
            },1700);

        }
        else{
            
            if(responseJson.lista){
                let lista = responseJson.lista;
                // Obtuvimos una lista de 1 o mas peliculas
                for(let pelicula in lista){

                    let newMovie = document.createElement('div');
                    newMovie.setAttribute('class','pelicula');


                    let name = document.createElement('div');
                    name.setAttribute('class','namePelicula');
                    let bN = document.createElement('b');
                    bN.textContent = 'Name:';
                    let divN = document.createElement('div');
                    divN.textContent = lista[pelicula].name;
                    name.append(bN);
                    name.append(divN);


                    let director = document.createElement('div');
                    director.setAttribute('class','directorPelicula');
                    let bD = document.createElement('b');
                    bD.textContent = "Director:";
                    let divD = document.createElement('div');
                    divD.textContent = lista[pelicula].director;
                    director.append(bD);
                    director.append(divD);


                    let release = document.createElement('div');
                    release.setAttribute('class','releasePelicula');
                    let bR = document.createElement('b');
                    bR.textContent = "Release:";
                    let divR = document.createElement('div');

                    let fechaLimpia = lista[pelicula].release.substring(0,10);
                    divR.textContent = fechaLimpia;
                    release.append(bR);
                    release.append(divR);

                    newMovie.append(name);
                    newMovie.append(director);
                    newMovie.append(release);

                    contenedor.append(newMovie);
                }
            }
        }
    }
}
