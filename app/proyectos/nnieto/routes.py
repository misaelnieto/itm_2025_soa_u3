from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func
from sqlmodel import Session, select

from app.main import DbSession

from .models import Movimiento
from .schemas import RespuestaOperacion, RespuestaSaldo


def _calcula_saldo(db: Session) -> int:
    result = db.exec(select(func.coalesce(func.sum(Movimiento.cantidad), 0)))
    return result.one_or_none()


router = APIRouter(
    prefix="/alcancia",
    tags=["alcancia"],
    responses={404: {"description": "Not found"}},
)


@router.get("/saldo", tags=["alcancia"])
def saldo(db: DbSession) -> RespuestaSaldo:
    """
    Calcula el saldo actual de la alcancía
    """
    # Equivalente a:
    # return {
    #     "operaciones": db.exec(select(func.count(Movimiento.id))).one_or_none(),
    #     "saldo": _calcula_saldo(db),
    # }
    return RespuestaSaldo(
        operaciones=db.exec(select(func.count(Movimiento.id))).one_or_none(),
        saldo=_calcula_saldo(db),
    )


@router.post("/deposito", tags=["alcancia"], status_code=status.HTTP_201_CREATED)
def deposito(cantidad: int, db: DbSession) -> RespuestaOperacion:
    """Realiza un depósito en la alcancía"""
    saldo_anterior = _calcula_saldo(db)
    db.add(Movimiento(cantidad=abs(cantidad)))
    db.commit()
    saldo_actual = _calcula_saldo(db)
    # Equivalente a:
    # return {"saldo_anterior": saldo_anterior, "saldo_actual": saldo_actual}
    return RespuestaOperacion(saldo_anterior=saldo_anterior, saldo_actual=saldo_actual)


@router.post("/retiro", tags=["alcancia"], status_code=status.HTTP_201_CREATED)
def retiro(cantidad: int, db: DbSession) -> RespuestaOperacion:
    """Realiza un retiro en la alcancía"""
    saldo_anterior = _calcula_saldo(db)
    if saldo_anterior < cantidad:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail={
                "error": "Fondos insuficientes",
                "explicacion": f"Usted desea retirar {cantidad} pero solo tiene {saldo_anterior}",
                "saldo": saldo_anterior,
            },
        )
    db.add(Movimiento(cantidad=-abs(cantidad)))
    db.commit()
    saldo_actual = _calcula_saldo(db)
    return RespuestaOperacion(saldo_anterior=saldo_anterior, saldo_actual=saldo_actual)


@router.get("/movimientos", tags=["alcancia"])
def movimientos(db: DbSession) -> list[Movimiento]:
    """Devuelve la lista de movimientos de la alcancía"""
    return db.exec(select(Movimiento)).all()
