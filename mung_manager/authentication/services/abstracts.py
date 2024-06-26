from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple

from attrs import define

from mung_manager.errors.exceptions import NotImplementedException
from mung_manager.users.models import User


class AbstractAuthService(ABC):
    @abstractmethod
    def generate_token(self, user: User) -> Tuple[str, str]:
        raise NotImplementedException()

    @abstractmethod
    def authenticate_user(self, user: User) -> User:
        raise NotImplementedException()


@define
class KakaoLoginCredentials:
    client_id: str
    client_secret: str


@define
class KakaoAccessToken:
    access_token: str


class AbstractKakaoLoginFlowService(ABC):
    @abstractmethod
    def get_token(self, code: str, redirect_uri: str) -> KakaoAccessToken:
        raise NotImplementedException()

    @abstractmethod
    def get_user_info(self, kakao_token: KakaoAccessToken) -> Dict[str, Any]:
        raise NotImplementedException()
