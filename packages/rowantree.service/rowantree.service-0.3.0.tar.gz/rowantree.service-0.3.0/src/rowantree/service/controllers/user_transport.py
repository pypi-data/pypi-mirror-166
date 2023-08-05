from rowantree.contracts import UserFeature

from ..contracts.requests.user_transport_request import UserTransportRequest
from .abstract_controller import AbstractController


class UserTransportController(AbstractController):
    def execute(self, user_guid: str, request: UserTransportRequest) -> UserFeature:
        return self.dao.user_transport(user_guid=user_guid, location=request.location)
