from typing import Optional

from pydantic import BaseModel

from .state import UserState


class User(BaseModel):
    guid: str
    state: Optional[UserState]
