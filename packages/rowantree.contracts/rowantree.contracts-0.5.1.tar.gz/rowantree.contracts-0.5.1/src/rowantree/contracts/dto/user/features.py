""" UserFeatures Definition """
from pydantic import BaseModel

from .feature import UserFeature


class UserFeatures(BaseModel):
    """
    UserFeatures DTO
    Defines a list of known user features (locations) of the game world.

    Attributes
    ----------
    features: list[UserFeature]
        A list of UserFeature objects.

    NOTE / TODO:
    This is a unique set of UserFeature objects.

    Due to the legacy implementation this has been brought forward as-is.
    However,
    We want to make this a dictionary in the future given the access pattern (and uniqueness constraint) of the data.
    """

    features: list[UserFeature]
