from ..contracts.responses.user_population_get_response import UserPopulationGetResponse
from .abstract_controller import AbstractController


class UserPopulationGetController(AbstractController):
    def execute(self, user_guid: str) -> UserPopulationGetResponse:
        return UserPopulationGetResponse(population=self.dao.user_population_by_guid_get(user_guid=user_guid))
