from pydantic import BaseModel

from .user_feature import UserFeature
from .user_income import UserIncome
from .user_notification import UserNotification
from .user_store import UserStore


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
