
from fastapi import APIRouter


api_router = APIRouter(
    prefix="/perritos",
    tags=["Perritos"],
    responses={404: {"description": "Not found"}},
)

@api_router.get("/woof", tags=["Perritos"])
def woof():
    return {
        'woof': 'patita',
    }