from rowantree.contracts import UserFeature

from .abstract_controller import AbstractController


class UserFeaturesActiveGetController(AbstractController):
    def execute(self, user_guid: str, details: bool) -> UserFeature:
        if details:
            feature: UserFeature = self.dao.user_active_feature_state_details_get(user_guid=user_guid)
        else:
            feature: UserFeature = self.dao.user_active_feature_get(user_guid=user_guid)
        return feature
