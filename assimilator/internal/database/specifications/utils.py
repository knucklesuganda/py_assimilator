from typing import Dict, List, Set, Tuple, Iterable

from assimilator.core.database.models import BaseModel


InternalContainers = (List, Set, Tuple, map)


def find_model_value(fields: Iterable[str], model: BaseModel):
    model_val = model

    for foreign_field in fields:
        if isinstance(model_val, InternalContainers):
            model_val = list(getattr(obj, foreign_field) for obj in model_val)
        elif isinstance(model_val, Dict):
            model_val = list(getattr(obj, foreign_field) for obj in model_val.values())
        else:
            model_val = getattr(model_val, foreign_field)

    return model_val
