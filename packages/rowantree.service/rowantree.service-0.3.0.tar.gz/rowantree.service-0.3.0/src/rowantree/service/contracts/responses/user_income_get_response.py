from pydantic import BaseModel

from rowantree.contracts import UserIncome


class UserIncomeGetResponse(BaseModel):
    income: list[UserIncome]
