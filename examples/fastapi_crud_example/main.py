from fastapi import FastAPI, Depends, HTTPException

from core.database import NotFoundError
from core.services import CRUDService
from examples.fastapi_crud_example.dependencies import get_service
from examples.fastapi_crud_example.schema import UserSchema

app = FastAPI()


@app.get('/')
async def user_list_route(service: CRUDService = Depends(get_service)):
    return service.list()


@app.get('/{id}')
async def user_get_route(id: int, service: CRUDService = Depends(get_service)):
    try:
        return service.get(id=id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Not found")


@app.post('/')
async def user_create_route(
    user_data: UserSchema,
    service: CRUDService = Depends(get_service),
):
    return service.create(user_data.dict())


@app.delete('/{id}')
async def user_delete_route(
    id: int,
    service: CRUDService = Depends(get_service),
):
    return service.delete(id=id)
