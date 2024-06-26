from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status

from mung_manager.common.base.api_managers import BaseAPIManager
from mung_manager.pet_kindergardens.apis.pet_kindergardens.apis import (
    PetKindergardenCreateAPI,
    PetKindergardenDetailAPI,
    PetKindergardenProfileAPI,
    PetKindergardenSearchAPI,
    PetKindergardenUpdateAPI,
)
from mung_manager.schemas.errors.authentications import (
    ErrorAuthenticationPasswordChangedSchema,
    ErrorAuthenticationUserDeletedSchema,
    ErrorAuthenticationUserInactiveSchema,
    ErrorAuthenticationUserNotFoundSchema,
    ErrorAuthorizationHeaderSchema,
    ErrorKakaoLocationFailedSchema,
    ErrorTokenIdentificationSchema,
)
from mung_manager.schemas.errors.commons import (
    ErrorAuthenticationFailedSchema,
    ErrorInvalidParameterFormatSchema,
    ErrorInvalidTokenSchema,
    ErrorNotAuthenticatedSchema,
    ErrorPermissionDeniedSchema,
    ErrorUnknownServerSchema,
)
from mung_manager.schemas.errors.pet_kindergardens import (
    ErrorPetKindergardenAlreadyExistsSchema,
    ErrorPetKindergardenNotFoundSchema,
)


class PetkindergardenListAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "POST": PetKindergardenCreateAPI.as_view,
    }

    @extend_schema(
        tags=["반려동물 유치원"],
        summary="반려동물 유치원 생성",
        description="""
        Rogic
            - 유저가 반려동물 유치원을 생성합니다.
        """,
        request=VIEWS_BY_METHOD["POST"]().cls.InputSerializer,
        responses={
            status.HTTP_200_OK: VIEWS_BY_METHOD["POST"]().cls.OutputSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[ErrorInvalidParameterFormatSchema, ErrorPetKindergardenAlreadyExistsSchema],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    ErrorAuthenticationFailedSchema,
                    ErrorNotAuthenticatedSchema,
                    ErrorInvalidTokenSchema,
                    ErrorAuthorizationHeaderSchema,
                    ErrorAuthenticationPasswordChangedSchema,
                    ErrorAuthenticationUserDeletedSchema,
                    ErrorAuthenticationUserInactiveSchema,
                    ErrorAuthenticationUserNotFoundSchema,
                    ErrorTokenIdentificationSchema,
                    ErrorKakaoLocationFailedSchema,
                ],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=OpenApiTypes.OBJECT, examples=[ErrorPermissionDeniedSchema]
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=OpenApiTypes.OBJECT, examples=[ErrorPetKindergardenNotFoundSchema]
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=OpenApiTypes.OBJECT, examples=[ErrorUnknownServerSchema]
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["POST"]()(request, *args, **kwargs)


class PetkindergardenDetailAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "GET": PetKindergardenDetailAPI.as_view,
        "PUT": PetKindergardenUpdateAPI.as_view,
    }

    @extend_schema(
        tags=["반려동물 유치원"],
        summary="반려동물 유치원 조회",
        description="""
        Rogic
            - 유저가 반려동물 유치원을 조회합니다.
        """,
        responses={
            status.HTTP_200_OK: VIEWS_BY_METHOD["GET"]().cls.OutputSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    ErrorAuthenticationFailedSchema,
                    ErrorNotAuthenticatedSchema,
                    ErrorInvalidTokenSchema,
                    ErrorAuthorizationHeaderSchema,
                    ErrorAuthenticationPasswordChangedSchema,
                    ErrorAuthenticationUserDeletedSchema,
                    ErrorAuthenticationUserInactiveSchema,
                    ErrorAuthenticationUserNotFoundSchema,
                    ErrorTokenIdentificationSchema,
                ],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=OpenApiTypes.OBJECT, examples=[ErrorPermissionDeniedSchema]
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=OpenApiTypes.OBJECT, examples=[ErrorPetKindergardenNotFoundSchema]
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=OpenApiTypes.OBJECT, examples=[ErrorUnknownServerSchema]
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["GET"]().as_view()(request, *args, **kwargs)

    @extend_schema(
        tags=["반려동물 유치원"],
        summary="반려동물 유치원 수정",
        description="""
        Rogic
            - 유저가 반려동물 유치원을 수정합니다.
        """,
        request=VIEWS_BY_METHOD["PUT"]().cls.InputSerializer,
        responses={
            status.HTTP_200_OK: VIEWS_BY_METHOD["PUT"]().cls.OutputSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=OpenApiTypes.OBJECT, examples=[ErrorInvalidParameterFormatSchema]
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    ErrorAuthenticationFailedSchema,
                    ErrorNotAuthenticatedSchema,
                    ErrorInvalidTokenSchema,
                    ErrorAuthorizationHeaderSchema,
                    ErrorAuthenticationPasswordChangedSchema,
                    ErrorAuthenticationUserDeletedSchema,
                    ErrorAuthenticationUserInactiveSchema,
                    ErrorAuthenticationUserNotFoundSchema,
                    ErrorTokenIdentificationSchema,
                    ErrorKakaoLocationFailedSchema,
                ],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=OpenApiTypes.OBJECT, examples=[ErrorPermissionDeniedSchema]
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=OpenApiTypes.OBJECT, examples=[ErrorPetKindergardenNotFoundSchema]
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=OpenApiTypes.OBJECT, examples=[ErrorUnknownServerSchema]
            ),
        },
    )
    def put(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["PUT"]().as_view()(request, *args, **kwargs)


class PetkindergardenSearchAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "GET": PetKindergardenSearchAPI.as_view,
    }

    @extend_schema(
        tags=["반려동물 유치원"],
        summary="네이버 반려동물 유치원 검색",
        description="""
        Rogic
            - 유저가 반려동물 유치원을 검색합니다.
        """,
        responses={
            status.HTTP_200_OK: VIEWS_BY_METHOD["GET"]().cls.OutputSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=OpenApiTypes.OBJECT, examples=[ErrorInvalidParameterFormatSchema]
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    ErrorAuthenticationFailedSchema,
                    ErrorNotAuthenticatedSchema,
                    ErrorInvalidTokenSchema,
                    ErrorAuthorizationHeaderSchema,
                    ErrorAuthenticationPasswordChangedSchema,
                    ErrorAuthenticationUserDeletedSchema,
                    ErrorAuthenticationUserInactiveSchema,
                    ErrorAuthenticationUserNotFoundSchema,
                    ErrorTokenIdentificationSchema,
                ],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=OpenApiTypes.OBJECT, examples=[ErrorPermissionDeniedSchema]
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=OpenApiTypes.OBJECT, examples=[ErrorUnknownServerSchema]
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["GET"]()(request, *args, **kwargs)


class PetkindergardenProfileAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "GET": PetKindergardenProfileAPI.as_view,
    }

    @extend_schema(
        tags=["반려동물 유치원"],
        summary="반려동물 유치원 프로필 조회",
        description="""
        Rogic
            - 유저가 반려동물 유치원 프로필을 조회합니다.
        """,
        responses={
            status.HTTP_200_OK: VIEWS_BY_METHOD["GET"]().cls.OutputSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    ErrorAuthenticationFailedSchema,
                    ErrorNotAuthenticatedSchema,
                    ErrorInvalidTokenSchema,
                    ErrorAuthorizationHeaderSchema,
                    ErrorAuthenticationPasswordChangedSchema,
                    ErrorAuthenticationUserDeletedSchema,
                    ErrorAuthenticationUserInactiveSchema,
                    ErrorAuthenticationUserNotFoundSchema,
                    ErrorTokenIdentificationSchema,
                ],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=OpenApiTypes.OBJECT, examples=[ErrorPermissionDeniedSchema]
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=OpenApiTypes.OBJECT, examples=[ErrorPetKindergardenNotFoundSchema]
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=OpenApiTypes.OBJECT, examples=[ErrorUnknownServerSchema]
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["GET"]()(request, *args, **kwargs)
