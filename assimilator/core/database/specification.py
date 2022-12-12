from abc import ABC, abstractmethod
from typing import Type


class Specification(ABC):
    and_specification: Type['AndSpecification']
    or_specification: Type['OrSpecification']
    not_specification: Type['NotSpecification']

    @abstractmethod
    def apply(self, query):
        raise NotImplementedError("Specification must specify apply()")

    def __call__(self, query):
        return self.apply(query)

    def __or__(self, other):
        return self.or_specification(first=self, second=other)

    def __and__(self, other):
        return self.and_specification(first=self, second=other)

    def __invert__(self):
        return self.not_specification(self)


class OrSpecification(Specification):
    def __init__(self, first: Specification, second: Specification):
        super(OrSpecification, self).__init__()
        self.first = first
        self.second = second

    def apply(self, query):
        return self.first(query) or self.second(query)


class AndSpecification(Specification):
    def __init__(self, first: Specification, second: Specification):
        super(AndSpecification, self).__init__()
        self.first = first
        self.second = second

    def apply(self, query):
        return self.first(query) and self.second(query)


class NotSpecification(Specification):
    def __init__(self, specification: Specification):
        super(NotSpecification, self).__init__()
        self.specification = specification

    def apply(self, query):
        return self.specification(query)
