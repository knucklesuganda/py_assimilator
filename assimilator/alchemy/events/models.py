from sqlalchemy.orm import registry
from sqlalchemy import Table, Column, Text, String


def create_event_table(mapper_registry: registry, table_name: str = "events") -> Table:
    return Table(
        table_name,
        mapper_registry.metadata,
        Column("id", Text(), primary_key=True),
        Column("event_name", String()),
        Column("event_data", Text()),
    )


def create_event_model(base_cls, table_name: str = "events"):
    class AlchemyEvent(base_cls):
        __tablename__ = table_name

        id = Column(Text(), primary_key=True)
        event_name = Column(String())
        event_data = Column(Text())

    return AlchemyEvent


__all__ = [
    'create_event_table',
    'create_event_model',
]
