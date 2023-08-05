from datetime import datetime

from pydantic import BaseModel

from .event import UserEvent


class UserNotification(BaseModel):
    index: int
    timestamp: datetime
    event: UserEvent
