from fastapi import FastAPI, Depends, HTTPException

from assimilator.core.services import CRUDService
from assimilator.core.patterns import ErrorWrapper
from assimilator.core.database import NotFoundError
from examples.databases.fastapi_crud_example.dependencies import get_service
from examples.databases.fastapi_crud_example.schema import UserCreateSchema

app = FastAPI()

api_error_wrapper = ErrorWrapper(
    error_mappings={
        NotFoundError: lambda error: HTTPException(status_code=404, detail="Not found"),
    },
    # default_error=lambda error: HTTPException(status_code=500, detail="Unknown error"),
)


@app.get('/users/')
def user_list_route(service: CRUDService = Depends(get_service)):
    return service.list()


@app.get('/users/{id}')
@api_error_wrapper.decorate
def user_get_route(id: str, service: CRUDService = Depends(get_service)):
    return service.get(id=str(id))


@app.post('/users/')
def user_create_route(user_data: UserCreateSchema, service: CRUDService = Depends(get_service)):
    return service.create(user_data.dict())


@app.delete('/users/{id}')
def user_delete_route(id: str, service: CRUDService = Depends(get_service)):
    return service.delete(id=id)


@app.put('/users/{id}')
def user_update_route(
    user_data: UserCreateSchema,
    id: str,
    service: CRUDService = Depends(get_service),
):
    return service.update(id=id, obj_data=user_data.dict())
