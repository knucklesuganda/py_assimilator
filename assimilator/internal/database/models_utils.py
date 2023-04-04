from typing import Type, Union

from pydantic import BaseModel as PydanticBaseModel

from assimilator.core.database.models import BaseModel


def get_model_relationship(model: Type[BaseModel], field_name: str) -> Union[Type[BaseModel], None]:
    try:
        return model.__fields__.get(field_name).type_
    except AttributeError:
        return None


def dict_to_internal_models(data: dict, model: Type[BaseModel]) -> dict:
    for field_name, value in dict(data).items():
        field_type = get_model_relationship(model, field_name)
        if field_type is None:
            continue
        elif not issubclass(field_type, PydanticBaseModel):
            continue

        if not isinstance(value, dict):
            data[field_name] = [
                field_type(**dict_to_internal_models(data=val_part, model=field_type))
                for val_part in value
            ]
        else:
            data[field_name] = field_type(**value)

    return data
