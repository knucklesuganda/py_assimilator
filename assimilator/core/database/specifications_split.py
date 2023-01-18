from abc import abstractmethod
from typing import Tuple, List, Iterable

from assimilator.core.database.specifications import SpecificationType


class SpecificationSplitMixin:
    """
    I found out that some data storages will not support specification
    that can only build queries and then execute them to get the results.

    Example: redis does not support simultaneous sorting and filtering with pagination, but SQLAlchemy can.
    We still want to sort results that come from Redis, so we split specifications into two categories:
    1) Specifications that run before the query is sent to the storage
    1) Specifications that run after the query is sent to the storage and work with a list of results

    This mixin allows you to use them in your repositories
    """

    @abstractmethod
    def _is_before_specification(self, specification: SpecificationType) -> bool:
        """ Checks that the specification provided is a specification that must be run before the query """
        raise NotImplementedError("is_before_specification() is not implemented")

    def _split_specifications(
        self, specifications: Iterable[SpecificationType], no_after_specs: bool = False
    ) -> Tuple[List[SpecificationType], List[SpecificationType]]:
        """
        Splits our specifications into two categories, so we can use them later.

        Sometimes you only want to use 'before_specs' and show your
        users that they cannot use 'after_specs' as they are useless.
        Example: using repository.get() with pagination. You only get one result, so pagination is useless.

        If that is the case, then turn on 'no_after_specs' and the function will raise a Warning() is there are
        any 'after_specs' present.
        """
        before_specs, after_specs = [], []

        for specification in specifications:
            if self._is_before_specification(specification):
                before_specs.append(specification)
            else:
                after_specs.append(specification)

        if no_after_specs and after_specs:
            raise Warning(
                "You are using after specifications in a function that bans them "
                "We cannot apply them, as the developers decided that after"
                " specifications do not fit in the function. "
                "Please, remove all the specifications that run after the results are obtained."
                "Examples: sorting, ordering, pagination, etc."
            )

        return before_specs, after_specs


__all__ = ['SpecificationSplitMixin']
