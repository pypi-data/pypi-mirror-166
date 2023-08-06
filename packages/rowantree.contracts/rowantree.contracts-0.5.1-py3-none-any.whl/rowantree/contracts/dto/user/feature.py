""" User Feature Definition """

from typing import Optional

from pydantic import BaseModel


class UserFeature(BaseModel):
    """
    UserFeature DTO
    Defines a user feature (world locations).

    Attributes
    ----------
    name: str
        The name of the feature.
    description: Optional[str]
        The description of the feature.
    """

    name: str
    description: Optional[str]
