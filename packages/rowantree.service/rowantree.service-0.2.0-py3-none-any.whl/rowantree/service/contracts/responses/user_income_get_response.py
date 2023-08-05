from pydantic import BaseModel

from ..dto.user_income import UserIncome


class UserIncomeGetResponse(BaseModel):
    income: list[UserIncome]
