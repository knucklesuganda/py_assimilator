from typing import Type, Union, Optional, TypeVar, List

from assimilator.core.patterns.error_wrapper import ErrorWrapper
from assimilator.internal.database.error_wrapper import InternalErrorWrapper
from assimilator.core.database import (
    Repository,
    SpecificationType,
    LazyCommand,
    InvalidQueryError,
    BaseModel,
    NotFoundError,
)
from assimilator.internal.database.specifications import InternalSpecificationList
from core.database import MultipleResultsError

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

        if query:   # Dict key was not provided, we must use other search parameters
            return self.session[query]

        found_models = self._apply_specifications(
            query=list(self.session.values()),
            specifications=specifications,
        )

        if not found_models:
            raise NotFoundError()
        elif len(found_models) != 1:
            raise MultipleResultsError()

        return found_models[0]

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

    def count(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: Optional[str] = None,
    ) -> Union[LazyCommand[int], int]:
        if specifications:
            return len(self.filter(*specifications, lazy=False, initial_query=initial_query))
        return len(self.session)


__all__ = [
    'InternalRepository',
]
