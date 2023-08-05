from rowantree.service.sdk import UserIncomeSetRequest

from ..controllers.abstract_controller import AbstractController


class UserIncomeSetController(AbstractController):
    def execute(self, user_guid: str, request: UserIncomeSetRequest) -> None:
        self.dao.user_income_set(user_guid=user_guid, transaction=request)
