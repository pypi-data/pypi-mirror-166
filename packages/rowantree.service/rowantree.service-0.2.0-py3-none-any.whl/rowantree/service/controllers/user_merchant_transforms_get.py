from ..contracts.responses.user_merchant_transforms_get_response import UserMerchantTransformsGetResponse
from .abstract_controller import AbstractController


class UserMerchantTransformsGetController(AbstractController):
    def execute(self, user_guid: str) -> UserMerchantTransformsGetResponse:
        return UserMerchantTransformsGetResponse(merchants=self.dao.user_merchant_transforms_get(user_guid=user_guid))
