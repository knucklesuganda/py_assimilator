import re
from typing import Type, Union

from assimilator.core.database.exceptions import NotFoundError
from assimilator.core.database import BaseRepository, SpecificationList, SpecificationType, LazyCommand
from assimilator.internal.database.specifications import InternalSpecification, InternalSpecificationList


class InternalRepository(BaseRepository):
    def __init__(
        self,
        session: dict,
        specifications: Type[SpecificationList] = InternalSpecificationList,
        initial_keyname: str = '',
    ):
        super(InternalRepository, self).__init__(
            session=session,
            initial_query=initial_keyname,
            specifications=specifications,
        )

    def get(self, *specifications: InternalSpecification, lazy: bool = False, initial_query=None):
        try:
            if lazy:
                return LazyCommand(self.get, *specifications, lazy=False, initial_query=initial_query)

            return self.session[self._apply_specifications(specifications, initial_query=initial_query)]
        except (KeyError, TypeError) as exc:
            raise NotFoundError(exc)

    def filter(self, *specifications: InternalSpecification, lazy: bool = False, initial_query=None):
        if lazy:
            return LazyCommand(self.filter, *specifications, lazy=False, initial_query=initial_query)

        if not specifications:
            return list(self.session.values())

        key_mask = self._apply_specifications(specifications, initial_query=initial_query)
        models = []
        for key, value in self.session.items():
            if re.match(key_mask, key):
                models.append(value)

        return models

    def save(self, obj):
        self.session[str(obj.id)] = obj

    def delete(self, obj):
        del self.session[str(obj.id)]

    def update(self, obj):
        self.session[str(obj.id)] = obj

    def is_modified(self, obj):
        return self.get(self.specifications.filter(obj.id)) == obj

    def refresh(self, obj):
        obj.value = self.get(self.specifications.filter(obj.id))

    def count(self, *specifications: SpecificationType, lazy: bool = False) -> Union[LazyCommand, int]:
        if lazy:
            return LazyCommand(self.count, *specifications, lazy=False)
        elif not specifications:
            return len(self.session)

        results: LazyCommand = self.filter(*specifications, lazy=True)
        return len(results())


__all__ = [
    'InternalRepository',
]
