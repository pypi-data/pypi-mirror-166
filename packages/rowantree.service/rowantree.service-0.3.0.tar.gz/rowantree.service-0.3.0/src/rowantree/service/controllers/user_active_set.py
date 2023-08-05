from ..contracts.requests.user_active_set_request import UserActiveSetRequest
from ..db.dao import DBDAO
from .abstract_controller import AbstractController


class UserActiveSetController(AbstractController):
    def __init__(self, dao: DBDAO):
        super().__init__(dao=dao)

    def execute(self, user_guid: str, request: UserActiveSetRequest) -> UserActiveSetRequest:
        self.dao.user_active_state_set(user_guid=user_guid, active=request.active)
        return request
