from typing import Type, Union, Optional, TypeVar, List

from assimilator.core.patterns.error_wrapper import ErrorWrapper
from assimilator.internal.database.error_wrapper import InternalErrorWrapper
from assimilator.core.database import (
    Repository,
    SpecificationType,
    LazyCommand,
    make_lazy,
    InvalidQueryError,
    BaseModel,
)
from assimilator.internal.database.specifications import InternalSpecificationList


ModelT = TypeVar("ModelT", bound=BaseModel)


class InternalRepository(Repository):
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

    @make_lazy
    def get(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: Optional[str] = None,
    ) -> Union[LazyCommand[ModelT], ModelT]:
        query = self._apply_specifications(
            query=self.get_initial_query(initial_query),
            specifications=specifications,
        )
        return self.session[query]

    @make_lazy
    def filter(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: Optional[str] = None,
    ) -> Union[LazyCommand[List[ModelT]], List[ModelT]]:
        return self._apply_specifications(
            query=list(self.session.values()),
            specifications=specifications,
        )

    def save(self, obj: Optional[ModelT] = None, **obj_data) -> ModelT:
        if obj is None:
            obj = self.model(**obj_data)

        self.session[obj.id] = obj
        return obj

    def delete(self, obj: Optional[ModelT] = None, *specifications: SpecificationType) -> None:
        obj, specifications = self._check_obj_is_specification(obj, specifications)

        if specifications:
            for model in self.filter(*specifications, lazy=True):
                del self.session[model.id]
        elif obj is not None:
            del self.session[obj.id]

    def update(
        self,
        obj: Optional[ModelT] = None,
        *specifications: SpecificationType,
        **update_values,
    ) -> None:
        obj, specifications = self._check_obj_is_specification(obj, specifications)

        if specifications:
            if not update_values:
                raise InvalidQueryError(
                    "You did not provide any update_values "
                    "to the update() yet provided specifications"
                )

            for model in self.filter(*specifications, lazy=True):
                model.__dict__.update(update_values)
                self.save(model)

        elif obj is not None:
            self.save(obj)

    def is_modified(self, obj: ModelT) -> bool:
        return self.get(self.specs.filter(id=obj.id)) == obj

    def refresh(self, obj: ModelT) -> None:
        fresh_obj = self.get(self.specs.filter(id=obj.id), lazy=False)
        obj.__dict__.update(fresh_obj.__dict__)

    @make_lazy
    def count(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
    ) -> Union[LazyCommand[int], int]:
        if specifications:
            return len(self.filter(*specifications, lazy=False))
        return len(self.session)


__all__ = [
    'InternalRepository',
]
