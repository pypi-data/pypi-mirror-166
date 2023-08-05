from pydantic import BaseModel

from .feature import UserFeature


class UserFeatures(BaseModel):
    features: list[UserFeature]
