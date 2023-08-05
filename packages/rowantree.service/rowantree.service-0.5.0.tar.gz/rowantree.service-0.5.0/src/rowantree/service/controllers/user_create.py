from rowantree.contracts import User

from .abstract_controller import AbstractController


class UserCreateController(AbstractController):
    def execute(self) -> User:
        return self.dao.user_create()
