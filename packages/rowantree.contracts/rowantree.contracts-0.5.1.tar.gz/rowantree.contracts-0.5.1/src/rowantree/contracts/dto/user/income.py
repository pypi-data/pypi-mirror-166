""" UserIncome Definition """

from typing import Optional

from pydantic import BaseModel


class UserIncome(BaseModel):
    """
    UserIncome DTO
    Define a user income source.

    Attributes
    ----------
    amount: int
        The amount (number of workers) of the income.
    name: str
        The name of the income.
    description: Optional[str]
        The optional description of the income.
    """

    amount: int
    name: str
    description: Optional[str]
