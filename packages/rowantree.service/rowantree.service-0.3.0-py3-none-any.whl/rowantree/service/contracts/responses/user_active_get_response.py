from pydantic import BaseModel


class UserActiveGetResponse(BaseModel):
    active: bool
