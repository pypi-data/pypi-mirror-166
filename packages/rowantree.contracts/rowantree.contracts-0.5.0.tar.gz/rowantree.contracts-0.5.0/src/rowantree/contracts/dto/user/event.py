from typing import Optional

from pydantic import BaseModel


class UserEvent(BaseModel):
    title: str
    text: Optional[list[str]]
    reward: Optional[dict[str, int]]
    curse: Optional[dict[str, int]]
