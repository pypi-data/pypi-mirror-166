from pydantic import BaseModel

from .feature import UserFeature
from .income import UserIncome
from .notification import UserNotification
from .store import UserStore


class UserState(BaseModel):
    active: bool
    stores: list[UserStore]
    income: list[UserIncome]
    features: list[str]
    active_features: UserFeature
    active_features_details: UserFeature
    population: int
    merchants: list[str]
    notifications: list[UserNotification]
