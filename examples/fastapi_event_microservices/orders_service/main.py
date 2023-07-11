from fastapi import FastAPI, Depends

from assimilator.core.services import CRUDService

from .dependencies import get_crud
from .schema import OrderCreateSchema


app = FastAPI()


@app.post('/orders/')
def create_order(order: OrderCreateSchema, crud: CRUDService = Depends(get_crud)):
    return crud.create(order.dict())
