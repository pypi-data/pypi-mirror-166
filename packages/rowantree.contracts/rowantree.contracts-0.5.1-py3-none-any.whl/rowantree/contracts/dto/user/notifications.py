""" UserNotifications Definition """

from pydantic import BaseModel

from .notification import UserNotification


class UserNotifications(BaseModel):
    """
    UserNotifications DTO
    Defines a list of user notifications.

    Attributes
    ----------
    notifications: list[UserNotification]
        A list of UserNotification objects.
    """

    notifications: list[UserNotification]
