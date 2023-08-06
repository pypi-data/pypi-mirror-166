""" Merchant Definition """
from pydantic import BaseModel


class Merchant(BaseModel):
    """
    Merchant DTO
    Defines the properties of a merchant.

    Attributes
    ----------
    name: str
        The name of the merchant.
    """

    name: str
