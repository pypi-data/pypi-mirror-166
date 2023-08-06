""" UserStore Definition """

from typing import Optional

from pydantic import BaseModel


class UserStore(BaseModel):
    """
    UserStore DTO
    Defines a user store.

    Attributes
    ----------
    name: str

    description: Optional[str]

    amount: int
        The amount of the user store.
    """

    name: str
    description: Optional[str]
    amount: int
