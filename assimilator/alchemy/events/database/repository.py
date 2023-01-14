from typing import Type, Optional

from sqlalchemy import Table
from sqlalchemy.orm import Query

from assimilator.alchemy import AlchemySpecificationList
from assimilator.alchemy.database.repository import AlchemyRepository
from assimilator.core.database import SpecificationList
from assimilator.core.patterns.error_wrapper import ErrorWrapper


class AlchemyOutboxRepository(AlchemyRepository):
    def __init__(
        self,
        session,
        event_model: Type[Table],
        model: Type[Table],
        initial_query: Optional[Query] = None,
        specifications: Type[SpecificationList] = AlchemySpecificationList,
        error_wrapper: ErrorWrapper = None,
    ):
        super(AlchemyOutboxRepository, self).__init__(
            session=session,
            initial_query=initial_query,
            model=model,
            specifications=specifications,
            error_wrapper=error_wrapper,
        )
        self.event_model = event_model

    def save(self, obj):
        super(AlchemyOutboxRepository, self).save(obj)
        super(AlchemyOutboxRepository, self).save(self.event_model(obj.outbox_event))


__all__ = [
    'AlchemyOutboxRepository',
]
