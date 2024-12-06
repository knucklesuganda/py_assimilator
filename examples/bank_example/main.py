from uuid import UUID

from fastapi import Depends, FastAPI

from assimilator.core.services import CRUDService
from examples.bank_example.dependencies import create_tables, create_user_service
from examples.bank_example.dto import UserData
from examples.bank_example.models import User
from examples.bank_example.services import (
    create_random_transactions,
    get_transactions_statistics,
)

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    create_tables()


@app.post("/")
async def register_route(
    user_data: UserData, service: CRUDService[User] = Depends(create_user_service)
) -> UUID:
    return service.create(obj_data=user_data.dict())


@app.get("/{id}")
async def get_user_route(
    id: UUID, service: CRUDService[User] = Depends(create_user_service)
):
    return service.get(id=id)


@app.get("/")
async def get_all_users_route(
    service: CRUDService[User] = Depends(create_user_service),
):
    return service.list()


@app.put("/{id}")
async def update_user_route(
    id: UUID,
    user_data: UserData,
    service: CRUDService[User] = Depends(create_user_service),
):
    return service.update(id=id, obj_data=user_data.dict())


@app.post("/transactions/random")
async def random_transactions_route():
    create_random_transactions()
    return {"created": True}


@app.get("/transactions/statistics")
async def transactions_statistics_route():
    return get_transactions_statistics()
