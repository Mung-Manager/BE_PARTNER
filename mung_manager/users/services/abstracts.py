from abc import ABC, abstractmethod
from collections import OrderedDict

from mung_manager.users.models import User


class AbstractUserService(ABC):
    @abstractmethod
    def create_social_user(
        self,
        email: str,
        name: str,
        social_id: str,
        phone_number: str,
        birth: object,
        gender: str,
        social_provider: int,
    ) -> User:
        pass

    @abstractmethod
    def update_user(self, user, data: OrderedDict) -> User:
        pass