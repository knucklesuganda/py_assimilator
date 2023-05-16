from typing import Iterable, Union, Any, Callable, TypeVar


def _split_fields(fields):
    raw_fields, parsed_fields = [], []

    for field in fields:
        if isinstance(field, str):
            parsed_fields.append(field)
        else:
            raw_fields.append(field)

    return raw_fields, parsed_fields


ModelT = TypeVar("ModelT")


def extract_fields(
    fields: Iterable[Union[str, Any]],
    model: ModelT,
    get_relationships: Callable[[ModelT], Iterable[ModelT]],
    get_model: Callable[[ModelT, str], ModelT],
):
    raw_fields, parsed_fields = _split_fields(fields)

    for raw_field in raw_fields:
        field_parts = raw_field.split('.')

        if len(field_parts) == 1:
            parsed_fields.append(getattr(model, raw_field))
        else:
            current_model = model

            for part in field_parts:
                current_model = getattr(current_model, raw_field) if \
                    part in get_relationships(current_model) else get_model(current_model, part)

    return parsed_fields


__all__ = [
    'extract_fields',
]
