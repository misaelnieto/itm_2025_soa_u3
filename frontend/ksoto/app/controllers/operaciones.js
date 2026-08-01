import fetch from 'node-fetch';



let regex_director = /^[a-zA-Z]+(?:\s[a-zA-Z]+)*$/;
let regex_id = /^[0-9]+$/;


async function agregarPelicula(solicitud,respuesta) {

    let name = solicitud.body.name;
    let director = solicitud.body.director;
    let release = solicitud.body.release;


    // Verificar campos invalidos
    let campos_validos = true;

    if(!regex_director.test(director)){
        campos_validos = false;
    }

    let releaseISO;
    try{
        releaseISO = new Date(release).toISOString();
    }
    catch(e){
        releaseISO = null;
        campos_validos = false;
    }




    // Si alguno de los campos es invalido, vamos a decirle al usuario que llene los datos de nuevo
    if(campos_validos == false){

        let answer = {
            error: "All fields must have valid information"
        }

        return respuesta.status(200).send(answer);
    }




    // Enviarla la data a la API
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


    if(!response.ok){

        console.log('Hubo un error con la comunicacion a la API');

        let answer = {
            error: "Something went wrong, please sorry"
        }

        return respuesta.status(200).send(answer);

    }else{

        let responseJson = await response.json();

        console.log(responseJson);    // < -- En este caso "agregarPelicula, solo nos dara informacion del proceso que el usuario no debe de ver"

        
        if(responseJson.status=="success"){

            let answer = {
                message: responseJson.comment
            }

            return respuesta.status(200).send(answer);

        }else{
            
            let answer = {
                error: responseJson.comment
            }

            return respuesta.status(200).send(answer);
        }

        

    }


    

    
}








async function eliminarPelicula(solicitud,respuesta){

    let id = solicitud.body.id;
    let name = solicitud.body.name;


    console.log(id);
    console.log(name);


    let campos_validos = true;

    if(regex_id.test(id)==false){
        campos_validos=false;
    }



    if(campos_validos==false){
        let answer = { error: "All fields must have valid information" }
        return respuesta.status(200).send(answer);
    }else{

        let response = await fetch(`http://localhost:8000/api/v1/ksoto/pelicula/movies/${id}/${name}`,{
            method:'DELETE',
            headers:{
                'Content-Type':'application/json'
            }
        });


        if(!response.ok){

            console.log('El servidor no se pudo comunicar con la API');

            let answer = { error: "UPSSS... Something went wrong" }
            return respuesta.status(200).send(answer);

        }else{

            let responseJson = await response.json();


            console.log(responseJson);    // <- es solo informacion de control para el backend


            if(responseJson.status=="success"){
                // Se elimino la pelicula exitosamente
                let answer = { message:responseJson.comment };
                return respuesta.status(200).send(answer);

            }else{
                // No se elimino la pelicula
                let answer = { error:responseJson.comment };
                return respuesta.status(200).send(answer);
            }
        }
    }

    

}








async function modificarPelicula(solicitud,respuesta){

    let id = solicitud.body.id;
    let name = solicitud.body.name;
    let new_name = solicitud.body.new_name;
    let new_director = solicitud.body.new_director;
    let fecha = solicitud.body.new_release;


    let campos_validos = true;

    if(regex_id.test(id)==false){
        campos_validos==false;
    }


    if(campos_validos==false){
        let answer = { error:'You must fill the data correct' };
        return respuesta.status(200).send(answer);
    }else{

        // Limpiar data
        if(new_name==null || new_name=="") new_name = null;
        if(new_director==null || new_director=="") new_director = null;
        

        // limpiar data
        let fechaISO = null;
        try{
            fechaISO = new Date(fecha).toISOString();
        }catch(e){
            fechaISO=null;
        }


        // mandar a llamar a la API
        let response = await fetch("http://localhost:8000/api/v1/ksoto/pelicula/movies",{
            method:'PUT',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                identificador:{
                    id:id,
                    name:name,
                },
                new_name:new_name,
                new_director:new_director,
                new_release:fechaISO
            })
        });


        if(!response.ok){
            console.log('El servidor no se pudo comunicar con la API');

            let answer = { error:'UPSSS... Something went wrong' };
            return respuesta.status(200).send(answer);
        }
        else{

            let responseJson = await response.json();

            console.log(responseJson);    // <- es solo informacion de control para el backend


            if(responseJson.status=="success"){

                let answer = { pelicula:responseJson.returnJson, comment:responseJson.comment };
                return respuesta.status(200).send(answer);

            }else{

                let answer = { error:responseJson.comment };
                return respuesta.status(200).send(answer);
            }

            
        }
    }



    

}



async function buscarPelicula(solicitud,respuesta){


    let id = solicitud.body.id;
    let name = solicitud.body.name;

    let campos_validos = true


    if(regex_id.test(id) == false){
        campos_validos = false;
    }


    if(campos_validos==false){

        let answer = {  error:'All fields must have valid information' };
        return respuesta.status(200).send(answer);

    }else{

        let response = await fetch(`http://localhost:8000/api/v1/ksoto/pelicula/movie/${id}/${name}`,{
            method:'GET',
            headers:{
                'Content-Type':'application/json'
            }
        });

        if(!response.ok){

            console.log('El servidor no se pudo comunicar con la API');
            let answer = { error:'UPSSS... Something went wrong' };
            return respuesta.status(200).send(answer);

        }else{

            let responseJson = await response.json();

            console.log(responseJson.returnJson); // <- informacion de control del backend

            if(responseJson.status=="success"){
                let answer = { pelicula:responseJson.returnJson, comment:responseJson.comment };
                return respuesta.status(200).send(answer);
            }else{
                let answer = { error: responseJson.comment };
                return respuesta.status(200).send(answer);
            }

        }
    }

}




async function obtenerPeliculas(solicitud,respuesta){

    let response = await fetch('http://localhost:8000/api/v1/ksoto/pelicula/movies',{
        method:'GET',
        headers:{
            'Content-Type':'application/json'
        }
    });

    if(!response.ok){
        console.log('El servidor no se pudo comunicar con la API');
        let answer = { error:'UPSSS... Something went wrong' };
        return respuesta.status(200).send(answer);
    }
    else{

        let responseJson = await response.json();

        if(responseJson.status=='success'){
            
            let answer = {
                lista:responseJson.returnJson
            };

            return respuesta.status(200).send(answer);
        }
        else{

            // Significa que no hubo exito
            let answer = { error: responseJson.comment };
            return respuesta.status(200).send(answer);
        }
    }
}



export const methods = {
    agregarPelicula,
    eliminarPelicula,
    modificarPelicula,
    buscarPelicula,
    obtenerPeliculas
}