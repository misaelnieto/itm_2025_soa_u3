import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
const _dirname = path.dirname(fileURLToPath(import.meta.url));
import { methods } from "./controllers/logica.js"


const app = express();

console.log(_dirname);

app.use(express.static(path.join(_dirname,'../static')));
app.use(express.json());


const port = 5090;


app.get('/home',(solicitud,respuesta)=>{
    respuesta.sendFile(path.join(_dirname,'../static/pages/home.html'));
})

app.listen(port, ()=>{
    console.log(`Servidor corriendo en el puerto ${port}`);
})

