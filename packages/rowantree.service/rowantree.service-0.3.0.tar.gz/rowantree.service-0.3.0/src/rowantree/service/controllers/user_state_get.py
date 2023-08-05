from starlette import status
from starlette.exceptions import HTTPException

from rowantree.contracts import UserFeature, UserIncome, UserNotification, UserStore
from rowantree.contracts.dto.user.state import UserState

from ..db.incorrect_row_count_error import IncorrectRowCountError
from .abstract_controller import AbstractController


class UserStateGetController(AbstractController):
    def execute(self, user_guid: str) -> UserState:
        # User Game State
        try:
            active: bool = self.dao.user_active_state_get(user_guid=user_guid)
        except IncorrectRowCountError as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") from error

        # User Stores (Inventory)
        stores: list[UserStore] = self.dao.user_stores_get(user_guid=user_guid)

        # User Income
        income: list[UserIncome] = self.dao.user_income_get(user_guid=user_guid)

        # Features
        features: list[str] = self.dao.user_features_get(user_guid=user_guid)

        # Population
        population: int = self.dao.user_population_by_guid_get(user_guid=user_guid)

        # Active Feature
        active_features: UserFeature = self.dao.user_active_feature_get(user_guid=user_guid)

        # Active Feature Details
        active_features_details: UserFeature = self.dao.user_active_feature_state_details_get(user_guid=user_guid)

        # Merchants
        merchants: list[str] = self.dao.user_merchant_transforms_get(user_guid=user_guid)

        # Notifications
        notifications: list[UserNotification] = self.dao.user_notifications_get(user_guid=user_guid)

        user_state: UserState = UserState(
            active=active,
            stores=stores,
            income=income,
            features=features,
            active_features=active_features,
            active_features_details=active_features_details,
            population=population,
            merchants=merchants,
            notifications=notifications,
        )
        return user_state
