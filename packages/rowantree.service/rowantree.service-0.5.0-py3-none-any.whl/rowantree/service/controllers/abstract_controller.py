from abc import ABC, abstractmethod
from typing import Any, Optional

from ..db.dao import DBDAO


class AbstractController(ABC):
    dao: DBDAO

    def __init__(self, dao: DBDAO):
        self.dao = dao

    @abstractmethod
    def execute(self, *args, **kwargs) -> Optional[Any]:
        """Should be implemented in the subclass"""
