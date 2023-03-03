from typing import TypeVar, Type

from sqlalchemy import inspect


T = TypeVar("T")


def get_model_from_relationship(model: T, relationship_name: str):
    foreign_prop = inspect(model).relationships[relationship_name]
    return foreign_prop.entity.class_, foreign_prop.uselist


def dict_to_models(data: dict, model: Type[T]) -> T:
    for relationship in inspect(model).relationships.keys():
        foreign_data = data.get(relationship)
        if foreign_data is None:
            continue

        foreign_model, is_list = get_model_from_relationship(
            model=model,
            relationship_name=relationship,
        )

        if not is_list and isinstance(foreign_data, dict):
            foreign_data = dict_to_models(data=foreign_data, model=foreign_model)
            foreign_data = foreign_model(**foreign_data)
        elif is_list:
            foreign_models = (
                foreign_data for foreign_data in foreign_data
                if isinstance(foreign_data, dict)
            )

            for i, foreign_part in enumerate(foreign_models):
                foreign_part = dict_to_models(data=foreign_part, model=foreign_model)
                foreign_data[i] = foreign_model(**foreign_part)

        data[relationship] = foreign_data

    return data
