from fastapi import FastAPI, Depends

from assimilator.core.services import CRUDService

from .dependencies import get_orders_crud, event_bus
from .schema import OrderCreateSchema

app = FastAPI()


@app.on_event('startup')
def startup_event():
    event_bus.consumer.start(threaded=True)


@app.post('/orders/')
def create_order(order: OrderCreateSchema, crud: CRUDService = Depends(get_orders_crud)):
    return crud.create({
        "status_id": 1,
        **order.dict(),
    })


@app.get('/orders/')
def list_orders(crud: CRUDService = Depends(get_orders_crud)):
    return crud.list()
