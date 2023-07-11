from fastapi import FastAPI, Depends

from assimilator.core.services import CRUDService

from .dependencies import get_crud
from .schema import UserCreateSchema


app = FastAPI()


@app.post('/users/')
def create_user_route(user: UserCreateSchema, crud: CRUDService = Depends(get_crud)):
    return crud.create(user.dict())


@app.get('/users/')
def list_users_route(crud: CRUDService = Depends(get_crud)):
    return crud.list()


@app.get('/users/{id}')
def get_user_route(id: int, crud: CRUDService = Depends(get_crud)):
    return crud.get(id=id)
