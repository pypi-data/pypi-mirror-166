from rowantree.contracts import UserIncomes

from .abstract_controller import AbstractController


class UserIncomeGetController(AbstractController):
    def execute(self, user_guid: str) -> UserIncomes:
        return self.dao.user_income_get(user_guid=user_guid)
