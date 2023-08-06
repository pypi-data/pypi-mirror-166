""" UserMerchants Definition """

from pydantic import BaseModel

from ..merchant.merchant import Merchant


class UserMerchants(BaseModel):
    """
    UserMerchants DTO
    Defines a list of user merchants.
    NOTE / TODO:
    This is a unique set of UserMerchants objects.

    Due to the legacy implementation this has been brought forward as-is.
    However,
    We want to make this a dictionary in the future given the access pattern (and uniqueness constraint) of the data.
    """

    merchants: list[Merchant]
