from typing import Type, Union, Optional, TypeVar, Collection

from sqlalchemy import func, select
from sqlalchemy.orm import Session, Query
from sqlalchemy.inspection import inspect

from assimilator.alchemy.database.error_wrapper import AlchemyErrorWrapper
from assimilator.core.database.exceptions import InvalidQueryError
from assimilator.alchemy.database.specifications import AlchemySpecificationList
from assimilator.core.database import BaseRepository, SpecificationList, \
    LazyCommand, SpecificationType, make_lazy
from assimilator.core.patterns.error_wrapper import ErrorWrapper


AlchemyModelT = TypeVar("AlchemyModelT")


class AlchemyRepository(BaseRepository):
    session: Session
    model: Type[AlchemyModelT]

    def __init__(
        self,
        session: Session,
        model: Type[AlchemyModelT],
        initial_query: Query = None,
        specifications: Type[SpecificationList] = AlchemySpecificationList,
        error_wrapper: Optional[ErrorWrapper] = None,
    ):
        super(AlchemyRepository, self).__init__(
            session=session,
            model=model,
            initial_query=initial_query if initial_query is not None else select(model),
            specifications=specifications,
            error_wrapper=error_wrapper or AlchemyErrorWrapper(),
        )

    @make_lazy
    def get(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: Query = None,
    ) -> Union[AlchemyModelT, LazyCommand[AlchemyModelT]]:
        query = self._apply_specifications(
            query=self.get_initial_query(initial_query),
            specifications=specifications,
        )
        return self.session.execute(query).one()[0]

    @make_lazy
    def filter(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: Query = None,
    ) -> Union[Collection[AlchemyModelT], LazyCommand[Collection[AlchemyModelT]]]:
        query = self._apply_specifications(
            query=self.get_initial_query(initial_query),
            specifications=specifications,
        )
        return [result[0] for result in self.session.execute(query)]

    def update(self, obj: AlchemyModelT) -> None:
        """ We don't do anything, as the object is going to be updated with the obj.key = value """

    def save(self, obj: AlchemyModelT) -> None:
        self.session.add(obj)

    def refresh(self, obj: AlchemyModelT) -> None:
        self.session.refresh(obj)

    def delete(self, obj: AlchemyModelT) -> None:
        self.session.delete(obj)

    def is_modified(self, obj: AlchemyModelT) -> bool:
        return self.session.is_modified(obj)

    @make_lazy
    def count(self, *specifications: SpecificationType, lazy: bool = False) -> Union[LazyCommand[int], int]:
        primary_keys = inspect(self.model).primary_key

        if not primary_keys:
            raise InvalidQueryError("Your repository model does not have"
                                    " any primary keys. We cannot use count()")

        return self.get(
            *specifications,
            lazy=False,
            query=select(func.count(getattr(self.model, primary_keys[0].name))),
        )


__all__ = [
    'AlchemyRepository',
]
