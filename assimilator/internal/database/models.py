from typing import Any

from pydantic import BaseModel


class InternalModel(BaseModel):
    id: Any
