from rowantree.contracts import UserFeatures

from .abstract_controller import AbstractController


class UserFeaturesGetController(AbstractController):
    def execute(self, user_guid: str) -> UserFeatures:
        return self.dao.user_features_get(user_guid=user_guid)
