from rowantree.contracts import UserStores

from .abstract_controller import AbstractController


class UserStoresGetController(AbstractController):
    def execute(self, user_guid: str) -> UserStores:
        return self.dao.user_stores_get(user_guid=user_guid)
