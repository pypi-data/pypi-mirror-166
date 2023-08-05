from pydantic import BaseModel

from ..merchant.merchant import Merchant
from .feature import UserFeature
from .income import UserIncome
from .notification import UserNotification
from .store import UserStore


class UserState(BaseModel):
    active: bool
    stores: list[UserStore]
    incomes: list[UserIncome]
    features: list[UserFeature]
    active_feature: UserFeature
    population: int
    merchants: list[Merchant]
    notifications: list[UserNotification]
