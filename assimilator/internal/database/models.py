from typing import Any

from pydantic import BaseModel

from assimilator.core.patterns.mixins import JSONParsedMixin


class InternalModel(JSONParsedMixin, BaseModel):
    id: Any
