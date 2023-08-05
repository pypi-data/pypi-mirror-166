from pydantic import BaseModel


class UserActiveSetRequest(BaseModel):
    active: bool
