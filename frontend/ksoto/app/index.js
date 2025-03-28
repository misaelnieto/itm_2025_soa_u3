import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
const _dirname = path.dirname(fileURLToPath(import.meta.url));
import { methods as operaciones } from './controllers/operaciones.js';


const app = express();

console.log(_dirname);

app.use(express.static(path.join(_dirname,'../static')));
app.use(express.json());



app.get('/inicio',(solicitud,respuesta)=>{
    respuesta.sendFile(path.join(_dirname,'../static/pages/main.html'));
})


app.get('/catalogo',(solicitud,respuesta)=>{
    respuesta.sendFile(path.join(_dirname,'../static/pages/catalogo.html'));
})




app.get('/operaciones/obtenerPeliculas',operaciones.obtenerPeliculas);
app.post('/operaciones/agregarPelicula',operaciones.agregarPelicula);
app.delete('/operaciones/eliminarPelicula',operaciones.eliminarPelicula);
app.put('/operaciones/modificarPelicula',operaciones.modificarPelicula);
app.post('/operaciones/buscarPelicula',operaciones.buscarPelicula);


const port = 5010;

app.listen(port,()=>{
    console.log(`Servidor corriendo en el puerto ${port}`);
})