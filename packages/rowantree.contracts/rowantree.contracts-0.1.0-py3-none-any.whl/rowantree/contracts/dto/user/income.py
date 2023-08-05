from typing import Optional

from pydantic import BaseModel


class UserIncome(BaseModel):
    amount: int
    name: str
    description: Optional[str]
