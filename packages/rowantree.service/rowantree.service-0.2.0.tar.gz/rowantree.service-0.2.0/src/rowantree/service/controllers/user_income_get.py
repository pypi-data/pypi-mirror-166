from ..contracts.responses.user_income_get_response import UserIncomeGetResponse
from .abstract_controller import AbstractController


class UserIncomeGetController(AbstractController):
    def execute(self, user_guid: str) -> UserIncomeGetResponse:
        return UserIncomeGetResponse(income=self.dao.user_income_get(user_guid=user_guid))
