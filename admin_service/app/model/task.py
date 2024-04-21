from pydantic import BaseModel, ConfigDict
from datetime import datetime, time
from typing import Optional

class TaskModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int]
    time: time
    text: str