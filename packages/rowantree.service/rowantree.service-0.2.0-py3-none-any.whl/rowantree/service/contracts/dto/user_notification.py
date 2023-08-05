from datetime import datetime

from pydantic import BaseModel

from .user_event import UserEvent


class UserNotification(BaseModel):
    index: int
    timestamp: datetime
    event: UserEvent
