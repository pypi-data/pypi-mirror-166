from pydantic import BaseModel


class UserCreateResponse(BaseModel):
    guid: str
