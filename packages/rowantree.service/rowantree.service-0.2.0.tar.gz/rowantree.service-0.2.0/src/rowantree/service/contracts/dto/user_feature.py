from typing import Optional

from pydantic import BaseModel


class UserFeature(BaseModel):
    name: str
    description: Optional[str]
