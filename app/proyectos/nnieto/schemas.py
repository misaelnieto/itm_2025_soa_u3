from pydantic import BaseModel


class PeticionCrearAlcancia(BaseModel):
    nombre: str


class RespuestaSaldo(BaseModel):
    operaciones: int 
    saldo: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "operaciones": 3,
                    "saldo": 5500,
                }
            ]
        }
    }

class RespuestaOperacion(BaseModel):
    saldo_anterior: int 
    saldo_actual: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "saldo_anterior": 5000,
                    "saldo_actual": 5500,
                }
            ]
        }
    }

