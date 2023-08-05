from pydantic import BaseModel


class UserPopulationGetResponse(BaseModel):
    population: int
