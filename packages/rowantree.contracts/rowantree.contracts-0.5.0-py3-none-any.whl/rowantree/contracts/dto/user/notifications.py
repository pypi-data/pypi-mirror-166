from pydantic import BaseModel

from .notification import UserNotification


class UserNotifications(BaseModel):
    notifications: list[UserNotification]
