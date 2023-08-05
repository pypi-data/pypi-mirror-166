from pydantic import BaseModel


class UserTransportRequest(BaseModel):
    location: str
