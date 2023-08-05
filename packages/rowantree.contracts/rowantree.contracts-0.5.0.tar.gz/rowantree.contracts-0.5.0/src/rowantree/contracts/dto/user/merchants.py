from pydantic import BaseModel

from ..merchant.merchant import Merchant


class UserMerchants(BaseModel):
    merchants: list[Merchant]
