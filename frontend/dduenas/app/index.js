import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
const _dirname = path.dirname(fileURLToPath(import.meta.url));


const app = express();

console.log(_dirname);

app.use(express.static(path.join(_dirname,'../static'), {
    setHeaders: (res, path) => {
        if (path.endsWith('.js')) {
            res.set('Content-Type', 'application/javascript');
        }
    }
}));
app.use(express.json());







app.get('/inicio',(solicitud,respuesta)=>{
    respuesta.sendFile(path.join(_dirname,'../static/pages/main.html'));
})

let port = 5090;

app.listen(port,()=>{
    console.log(`Servidor corriendo en el puerto ${port}`);
});