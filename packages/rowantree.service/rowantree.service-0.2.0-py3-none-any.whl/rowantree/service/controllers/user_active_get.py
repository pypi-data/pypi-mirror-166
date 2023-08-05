import logging

from ..contracts.responses.user_active_get_response import UserActiveGetResponse
from ..db.dao import DBDAO
from ..db.incorrect_row_count_error import IncorrectRowCountError
from .abstract_controller import AbstractController


class UserActiveGetController(AbstractController):
    def __init__(self, dao: DBDAO):
        super().__init__(dao=dao)

    def execute(self, user_guid: str) -> UserActiveGetResponse:
        # If the requested user does not exist we do not expose this in the response. (information leakage).
        # If the user is not found or is inactive we return an inactive response.
        try:
            user_active_state: bool = self.dao.user_active_state_get(user_guid=user_guid)
            logging.debug("user state requested for: {%s}, result: {%i}", user_guid, user_active_state)
        except IncorrectRowCountError as error:
            logging.debug("caught: {%s}", str(error))
            user_active_state: bool = False

        return UserActiveGetResponse(active=user_active_state)
