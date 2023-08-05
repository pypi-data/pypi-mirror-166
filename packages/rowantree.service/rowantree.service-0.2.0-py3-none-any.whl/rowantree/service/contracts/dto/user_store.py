from typing import Optional

from pydantic import BaseModel


class UserStore(BaseModel):
    name: str
    description: Optional[str]
    amount: int
