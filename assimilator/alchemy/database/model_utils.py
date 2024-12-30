from typing import Type, TypeVar

from sqlalchemy import inspect
from sqlalchemy.orm import Query

AlchemyModelT = TypeVar("AlchemyModelT")


def get_model_from_relationship(
    model: AlchemyModelT,
    relationship_name: str,
) -> tuple[Type[AlchemyModelT], bool]:
    foreign_prop = inspect(model).relationships[relationship_name]
    return foreign_prop.entity.class_, foreign_prop.uselist


def dict_to_alchemy_models(data: dict, model: Type[AlchemyModelT]) -> dict:
    for relationship in inspect(model).relationships.keys():
        foreign_data = data.get(relationship)
        if foreign_data is None:
            continue

        foreign_model, is_list = get_model_from_relationship(
            model=model,
            relationship_name=relationship,
        )

        if not is_list and isinstance(foreign_data, dict):
            foreign_data = dict_to_alchemy_models(data=foreign_data, model=foreign_model)
            foreign_data = foreign_model(**foreign_data)
        elif is_list:
            foreign_models = (
                foreign_data for foreign_data in foreign_data
                if isinstance(foreign_data, dict)
            )

            for i, foreign_part in enumerate(foreign_models):
                foreign_part = dict_to_alchemy_models(data=foreign_part, model=foreign_model)
                foreign_data[i] = foreign_model(**foreign_part)

        data[relationship] = foreign_data

    return data


def is_querying_model(query: Query, model: type[AlchemyModelT]) -> bool:
    return any(
        isinstance(entity, Query._entity_registry) and entity.entity_zero.class_ is model
        for entity in query._entities
    )

