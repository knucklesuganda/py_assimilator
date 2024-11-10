from uuid import UUID

from fastapi import FastAPI, Depends

from assimilator.core.database import UnitOfWork
from assimilator.core.services import CRUDService
from examples.bank_example.dependencies import (
    create_user_service,
    create_tables,
    create_users_uow,
    create_transactions_uow,
)
from examples.bank_example.dto import UserData
from examples.bank_example.models import User
from examples.bank_example.services import create_random_transactions


app = FastAPI()


@app.on_event('startup')
async def on_startup():
    create_tables()


@app.post("/")
async def register_route(
    user_data: UserData,
    service: CRUDService[User] = Depends(create_user_service)
) -> UUID:
    return service.create(obj_data=user_data.dict())


@app.get("/{id}")
async def get_user_route(id: UUID, service: CRUDService[User] = Depends(create_user_service)):
    return service.get(id=id)


@app.get('/')
async def get_all_users_route(service: CRUDService[User] = Depends(create_user_service)):
    return service.list()


@app.put("/{id}")
async def update_user_route(
    id: UUID,
    user_data: UserData,
    service: CRUDService[User] = Depends(create_user_service),
):
    return service.update(id=id, obj_data=user_data.dict())


@app.post('/transactions/random')
async def random_transactions_route(
    user_uow: UnitOfWork = Depends(create_users_uow),
    transaction_uow: UnitOfWork = Depends(create_transactions_uow),
):
    create_random_transactions()
    return {"created": True}
