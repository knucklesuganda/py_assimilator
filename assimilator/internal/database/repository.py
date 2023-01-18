import re
from typing import Type, Union, Optional, Iterable, TypeVar, List, Tuple

from assimilator.core.database.repository import make_lazy
from assimilator.internal.database.models import InternalModel
from assimilator.core.patterns.error_wrapper import ErrorWrapper
from assimilator.internal.database.error_wrapper import InternalErrorWrapper
from assimilator.internal.database.specifications import InternalSpecificationList, internal_filter
from assimilator.core.database import BaseRepository, SpecificationType, LazyCommand, SpecificationSplitMixin

ModelT = TypeVar("ModelT", bound=InternalModel)


class InternalRepository(SpecificationSplitMixin, BaseRepository):
    session: dict
    model: Type[ModelT]

    def __init__(
        self,
        session: dict,
        model: Type[ModelT],
        initial_query: Optional[str] = '',
        specifications: Type[InternalSpecificationList] = InternalSpecificationList,
        error_wrapper: Optional[ErrorWrapper] = None,
    ):
        super(InternalRepository, self).__init__(
            model=model,
            session=session,
            initial_query=initial_query,
            specifications=specifications,
            error_wrapper=error_wrapper or InternalErrorWrapper(),
        )

    def _is_before_specification(self, specification: SpecificationType) -> bool:
        return specification is internal_filter or specification is self.specs.filter

    @make_lazy
    def get(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: Optional[str] = None,
    ) -> Union[LazyCommand[ModelT], ModelT]:
        before_specs, _ = self._split_specifications(specifications, no_after_specs=True)

        query = self._apply_specifications(
            query=self.get_initial_query(initial_query),
            specifications=before_specs,
        )
        return self.session[query]

    @make_lazy
    def filter(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: Optional[str] = None,
    ) -> Union[LazyCommand[List[ModelT]], List[ModelT]]:
        before_specs, after_specs = self._split_specifications(specifications)

        if not before_specs:    # No filters, get all the data from the session
            models = list(self.session.values())
        else:
            models = []
            key_mask = self._apply_specifications(
                query=self.get_initial_query(initial_query),
                specifications=before_specs,
            )

            for key, value in self.session.items():
                if re.match(key_mask, key):
                    models.append(value)

        return self._apply_specifications(query=models, specifications=after_specs)

    def save(self, obj: ModelT) -> None:
        self.session[obj.id] = obj

    def delete(self, obj: ModelT) -> None:
        del self.session[obj.id]

    def update(self, obj: ModelT) -> None:
        self.save(obj)

    def is_modified(self, obj: ModelT) -> bool:
        return self.get(self.specs.filter(id=obj.id)) == obj

    def refresh(self, obj: ModelT) -> None:
        fresh_obj = self.get(self.specs.filter(id=obj.id), lazy=False)
        obj.__dict__.update(fresh_obj.__dict__)

    @make_lazy
    def count(self, *specifications: SpecificationType, lazy: bool = False) -> Union[LazyCommand[int], int]:
        if specifications:
            return len(self.filter(*specifications, lazy=False))
        return len(self.session)


__all__ = [
    'InternalRepository',
]
