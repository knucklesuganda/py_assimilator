from typing import Type, TypeVar

from sqlalchemy import inspect

T = TypeVar("T")


def get_model_from_relationship(model: T, relationship_name: str):
    foreign_prop = inspect(model).relationships[relationship_name]
    return foreign_prop.entity.class_, foreign_prop.uselist


def dict_to_alchemy_models(data: dict, model: Type[T]) -> dict:
    model_data: dict = {}

    for key, value in data.items():
        if key in inspect(model).relationships.keys():
            relationship = inspect(model).relationships[key]
            related_model = relationship.mapper.class_

            if relationship.uselist:
                model_data[key] = [
                    dict_to_alchemy_models(data=item, model=related_model)
                    for item in value
                ]
            else:
                model_data[key] = dict_to_alchemy_models(
                    data=value, model=related_model
                )
        else:
            model_data[key] = value

    return model_data
