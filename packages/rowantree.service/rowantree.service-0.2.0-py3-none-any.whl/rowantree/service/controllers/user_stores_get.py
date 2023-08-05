from ..contracts.responses.user_stores_get_response import UserStoresGetResponse
from .abstract_controller import AbstractController


class UserStoresGetController(AbstractController):
    def execute(self, user_guid: str) -> UserStoresGetResponse:
        return UserStoresGetResponse(stores=self.dao.user_stores_get(user_guid=user_guid))
