from ..contracts.responses.user_features_get_response import UserFeaturesGetResponse
from .abstract_controller import AbstractController


class UserFeaturesGetController(AbstractController):
    def execute(self, user_guid: str) -> UserFeaturesGetResponse:
        return UserFeaturesGetResponse(features=self.dao.user_features_get(user_guid=user_guid))
