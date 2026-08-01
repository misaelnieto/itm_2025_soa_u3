let fillDataAlerrt = document.getElementsByClassName('fillData')[0];
let contenidoFDA = document.getElementsByClassName('contenidoFDA')[0];
let addForm = document.getElementById('agregarPelicula');
let deleteForm = document.getElementById('eliminarPelicula');
let changeForm = document.getElementById('modificarPelicula');
let selectForm = document.getElementById('identificarPelicula');
let peliculaAlert = document.getElementsByClassName('peliculaAlert')[0];
let spanNM = document.getElementById('spanNM');
let spanDM = document.getElementById('spanDM');
let spanRM = document.getElementById('spanRM');
let titt_content = document.getElementById('titt_content');
let listaForm = [addForm,deleteForm,changeForm,selectForm];



function closeForm(button){
    formulario = button.parentNode;
    formulario.style.display="none";
    formulario.reset();
}


function ShutDown(id){
    for(let formulario in listaForm){
        if(listaForm[formulario].id!=id){
            listaForm[formulario].style.display = "none";
            listaForm[formulario].reset();
        }
    }
}


let operacion1 = document.getElementById('op1');
operacion1.addEventListener("click",()=>{
    ShutDown(addForm.id);
    addForm.style.display = "inline-block";
});


let operacion2 = document.getElementById('op2');
operacion2.addEventListener("click",()=>{
    ShutDown(changeForm.id);
    changeForm.style.display = "inline-block";
});


let operacion3 = document.getElementById('op3');
operacion3.addEventListener("click",()=>{
    ShutDown(deleteForm.id);
    deleteForm.style.display = "inline-block";
});


let operacion4 = document.getElementById('op4');
operacion4.addEventListener("click",()=>{
    ShutDown(selectForm.id);
    selectForm.style.display = "inline-block";
});






addForm.addEventListener('submit',async (e)=>{
    e.preventDefault();

    let nombre = e.target.elements['name'].value;
    let director = e.target.elements['director'].value;
    let fecha = e.target.elements['release'].value

    if(!nombre || !director || !fecha){

        contenidoFDA.textContent = "You must fill in all the data!!";
        fillDataAlerrt.style.display = "inline-block";

        setTimeout(()=>{
                fillDataAlerrt.style.display = "none";
        }, 1700);

    }else{


        let response = await fetch("http://localhost:5010/operaciones/agregarPelicula",{

            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                name:nombre,
                director:director,
                release:fecha
            })

        });


        if(!response.ok){

            console.log("No se encontro el servidor");

        }else{

            let responseJson = await response.json();

            if(responseJson.error){

                contenidoFDA.textContent = responseJson.error;
                fillDataAlerrt.style.display = "inline-block";

                setTimeout(()=>{
                        fillDataAlerrt.style.display = "none";
                }, 1700);

            }else{

                if(responseJson.message){

                    contenidoFDA.textContent = responseJson.message;
                    fillDataAlerrt.style.display = "inline-block";
    
                    setTimeout(()=>{
                            fillDataAlerrt.style.display = "none";
                    }, 1700);
    
                }

            }  

        }
    }

    
});








deleteForm.addEventListener("submit",async(e)=>{

    e.preventDefault();
    

    let id = e.target.elements['id'].value;
    let nombre = e.target.elements['name'].value;


    if(!id || !nombre){

        contenidoFDA.textContent = "You must fill in all the data!!";
        fillDataAlerrt.style.display = "inline-block";

        setTimeout(()=>{
                fillDataAlerrt.style.display = "none";
        }, 1700);

    }else{

        let response = await fetch("http://localhost:5010/operaciones/eliminarPelicula",{

            method:'DELETE',
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                id:id,
                name:nombre
            })
    
        });
    
    
        if(!response.ok){
            console.log("No se encontro la API");
        }else{
    
            let responseJson = await response.json();
    
            if(responseJson){
                console.log(responseJson);
            }
        }
    }

    


});







changeForm.addEventListener("submit",async(e)=>{

    e.preventDefault();

    let id = e.target.elements['id'].value;
    let nombre = e.target.elements['name'].value;


    if(!id || !nombre){
        
        contenidoFDA.textContent = "You must fill in the ID and name fields!!";
        fillDataAlerrt.style.display = "inline-block";

        setTimeout(()=>{
                fillDataAlerrt.style.display = "none";
        }, 1700);

    }else{

        let new_name = e.target.elements['new_name'].value;
        let new_director = e.target.elements['new_director'].value;
        let fecha = e.target.elements['new_release'].value;
    

        let response = await fetch("http://localhost:5010/operaciones/modificarPelicula",{
            method:'PUT',
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                id:id,
                name:nombre,
                new_name : new_name,
                new_director : new_director,
                new_release : fecha
            })
        });


        if(!response.ok){
            console.log("Hubo un error, no se encontro la API");
        }else{

            let responseJson = await response.json();

            if(responseJson.pelicula){

                // Los datos de la pelicula fueron cambiados con exito
                spanNM.textContent = responseJson.pelicula.name;
                spanDM.textContent = responseJson.pelicula.director;
                let fechaLimpia = responseJson.pelicula.release.substring(0,10);
                spanRM.textContent = fechaLimpia;
                titt_content.textContent = responseJson.comment;

                peliculaAlert.style.display = "inline-block";
                setTimeout(()=>{
                    peliculaAlert.style.display = "none";
                },1700);

            }else{

                if(responseJson.error){

                    contenidoFDA.textContent = responseJson.error;
                    fillDataAlerrt.style.display = "inline-block";

                    setTimeout(()=>{
                            fillDataAlerrt.style.display = "none";
                    }, 1700);

                }
            }
        }

    }


    
});








selectForm.addEventListener("submit",async(e)=>{

    e.preventDefault();
    

    let id = e.target.elements['id'].value;
    let nombre = e.target.elements['name'].value;


    if(!id || !nombre){

        contenidoFDA.textContent = "You must fill in all the data!!";
        fillDataAlerrt.style.display = "inline-block";

        setTimeout(()=>{
                fillDataAlerrt.style.display = "none";
        }, 1700);

    }else{


        let response = await fetch('http://localhost:5010/operaciones/buscarPelicula',{

            method:'POST',
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                id:id,
                name:nombre
            })
        });
    
    
        if(!response.ok){
            console.log("No se encontro la API");
        }else{
    
            let responseJson = await response.json();

            if(responseJson.pelicula){

                console.log(responseJson.pelicula);

                // Mostrar los datos obtenidos por la busqueda
                spanNM.textContent = responseJson.pelicula.name;
                spanDM.textContent = responseJson.pelicula.director;
                let fechaLimpia = responseJson.pelicula.release.substring(0,10);
                spanRM.textContent = fechaLimpia;
                titt_content.textContent = responseJson.comment;

                peliculaAlert.style.display = "inline-block";
                setTimeout(()=>{
                    peliculaAlert.style.display = "none";
                },1700);

            }else{

                if(responseJson.error){

                    contenidoFDA.textContent = responseJson.error;
                    fillDataAlerrt.style.display = "inline-block";

                    setTimeout(()=>{
                            fillDataAlerrt.style.display = "none";
                    }, 1700);

                }
            }
        }
    }

    


});


