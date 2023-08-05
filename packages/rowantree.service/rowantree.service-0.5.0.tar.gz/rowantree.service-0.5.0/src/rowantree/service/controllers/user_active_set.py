from rowantree.contracts import UserActive

from ..db.dao import DBDAO
from .abstract_controller import AbstractController


class UserActiveSetController(AbstractController):
    def __init__(self, dao: DBDAO):
        super().__init__(dao=dao)

    def execute(self, user_guid: str, request: UserActive) -> UserActive:
        self.dao.user_active_state_set(user_guid=user_guid, active=request.active)
        return request
