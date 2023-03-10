import json
from uuid import uuid4, UUID
from typing import (
    Type, TypeVar, ClassVar, Union,
    Optional, Callable, Any, AbstractSet,
    Mapping, Dict,
)

from pydantic import BaseModel as PydanticBaseModel, Extra, ValidationError, Field

from assimilator.core.exceptions import ParsingError


T = TypeVar("T", bound='BaseModel')
AbstractSetIntStr = AbstractSet[Union[int, str]]
MappingIntStrAny = Mapping[Union[int, str], Any]


class BaseModel(PydanticBaseModel):
    id: str = Field(allow_mutation=False)

    class AssimilatorConfig(PydanticBaseModel, extra=Extra.allow):
        autogenerate_id: ClassVar[bool] = True
        exclude: ClassVar[set] = None

    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True

    def __hash__(self):
        return UUID(self.id).int

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not issubclass(cls.AssimilatorConfig, BaseModel.AssimilatorConfig):
            base_configs = [
                base_class.AssimilatorConfig for base_class in cls.mro()
                if hasattr(base_class, 'AssimilatorConfig')
            ]

            class InheritedConfig(*base_configs):
                ...

            cls.AssimilatorConfig = InheritedConfig

        return cls

    def generate_id(self, **kwargs) -> str:
        return str(uuid4())

    def __init__(self, **kwargs):
        if self.AssimilatorConfig.autogenerate_id and kwargs.get('id') is None:
            kwargs['id'] = self.generate_id(**kwargs)

        super(BaseModel, self).__init__(**kwargs)

    @classmethod
    def loads(cls: Type['T'], data: str) -> 'T':
        try:
            return cls(**json.loads(data))
        except (ValidationError, TypeError) as exc:
            raise ParsingError(exc)

    def json(
        self,
        *,
        include: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']] = None,
        exclude: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        encoder: Optional[Callable[[Any], Any]] = None,
        models_as_dict: bool = True,
        **dumps_kwargs: Any,
    ) -> str:
        return super(BaseModel, self).json(
            include=include,
            exclude={*(exclude or []), *(self.AssimilatorConfig.exclude or [])},
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            encoder=encoder,
            models_as_dict=models_as_dict,
            **dumps_kwargs,
        )

    def dict(
        self,
        *,
        include: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']] = None,
        exclude: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> Dict[str, Any]:
        return super(BaseModel, self).dict(
            include=include,
            exclude={*(exclude or []), *(self.AssimilatorConfig.exclude or [])},
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )


__all__ = [
    'BaseModel',
]
