import re
from typing import Type, Union, Optional, Tuple

from assimilator.core.database.repository import make_lazy
from assimilator.internal.database.models import InternalModel
from assimilator.core.patterns.error_wrapper import ErrorWrapper
from assimilator.internal.database.error_wrapper import InternalErrorWrapper
from assimilator.internal.database.specifications import InternalSpecificationList, internal_filter
from assimilator.core.database import BaseRepository, SpecificationList, SpecificationType, LazyCommand


class InternalRepository(BaseRepository):
    def __init__(
        self,
        session: dict,
        model: Type[InternalModel],
        initial_query: Optional[str] = '',
        specifications: Type[SpecificationList] = InternalSpecificationList,
        error_wrapper: Optional[ErrorWrapper] = None,
    ):
        super(InternalRepository, self).__init__(
            model=model,
            session=session,
            initial_query=initial_query,
            specifications=specifications,
        )
        self.error_wrapper = error_wrapper if error_wrapper is not None else InternalErrorWrapper()

    def check_before_specification(self, specification: SpecificationType):
        """ Checks that the specification provided is a specification that must be run before the query """
        return specification is internal_filter

    def __parse_specifications(self, specifications: Tuple):
        before_specs, after_specs = [], []

        for specification in specifications:
            if self.check_before_specification(specification):
                before_specs.append(specification)
            else:
                after_specs.append(specification)

        return before_specs, after_specs

    @make_lazy
    def get(self, *specifications: SpecificationType, lazy: bool = False, initial_query=None):
        with self.error_wrapper:
            query = self._apply_specifications(
                query=self.get_initial_query(initial_query),
                specifications=specifications,
            )
            return self.session[query]

    @make_lazy
    def filter(self, *specifications: SpecificationType, lazy: bool = False, initial_query=None):
        with self.error_wrapper:
            before_specs, after_specs = self.__parse_specifications(specifications)

            if not before_specs:
                models = list(self.session.values())
            else:
                models = []
                key_mask = self._apply_specifications(
                    query=self.get_initial_query(initial_query),
                    specifications=before_specs
                )

                for key, value in self.session.items():
                    if re.match(key_mask, key):
                        models.append(value)

            return self._apply_specifications(query=models, specifications=after_specs)

    def save(self, obj):
        self.session[obj.id] = obj

    def delete(self, obj):
        del self.session[obj.id]

    def update(self, obj):
        self.save(obj)

    def is_modified(self, obj):
        return self.get(self.specs.filter(id=obj.id)) == obj

    def refresh(self, obj):
        fresh_obj = self.get(self.specs.filter(id=obj.id), lazy=False)
        obj.__dict__.update(fresh_obj.__dict__)

    @make_lazy
    def count(self, *specifications: SpecificationType, lazy: bool = False) -> Union[LazyCommand, int]:
        if specifications:
            return len(self.filter(*specifications, lazy=False))
        return len(self.session)


__all__ = [
    'InternalRepository',
]
