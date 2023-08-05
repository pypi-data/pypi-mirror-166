from pydantic import BaseModel

from .action import Action


class ActionQueue(BaseModel):
    queue: list[Action]
