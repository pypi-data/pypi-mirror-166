from ..contracts.responses.user_create_response import UserCreateResponse
from .abstract_controller import AbstractController


class UserCreateController(AbstractController):
    def execute(self) -> UserCreateResponse:
        return UserCreateResponse(guid=self.dao.user_create())
