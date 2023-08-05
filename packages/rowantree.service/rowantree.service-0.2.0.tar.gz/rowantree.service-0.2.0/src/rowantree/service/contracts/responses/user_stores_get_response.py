from pydantic import BaseModel


class UserStoresGetResponse(BaseModel):
    stores: list[str]
