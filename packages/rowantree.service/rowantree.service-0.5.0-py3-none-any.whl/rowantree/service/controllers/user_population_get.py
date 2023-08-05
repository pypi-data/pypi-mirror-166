from rowantree.contracts import UserPopulation

from .abstract_controller import AbstractController


class UserPopulationGetController(AbstractController):
    def execute(self, user_guid: str) -> UserPopulation:
        return self.dao.user_population_by_guid_get(user_guid=user_guid)
