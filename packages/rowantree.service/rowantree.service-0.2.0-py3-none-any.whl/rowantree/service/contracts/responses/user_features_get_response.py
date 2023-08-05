from pydantic import BaseModel


class UserFeaturesGetResponse(BaseModel):
    features: list[str]
