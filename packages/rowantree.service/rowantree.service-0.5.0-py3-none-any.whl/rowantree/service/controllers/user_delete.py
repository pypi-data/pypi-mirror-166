from typing import Any

from .abstract_controller import AbstractController


class UserDeleteController(AbstractController):
    def execute(self, user_guid: str) -> Any:
        return self.dao.user_delete(user_guid=user_guid)
