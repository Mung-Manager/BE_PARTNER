from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from mung_manager.apis.mixins import APIAuthMixin
from mung_manager.apis.pagination import LimitOffsetPagination, get_paginated_data
from mung_manager.common.base.serializers import BaseSerializer
from mung_manager.common.constants import SYSTEM_CODE
from mung_manager.common.selectors import (
    check_object_or_not_found,
    get_object_or_not_found,
)
from mung_manager.common.utils import inline_serializer
from mung_manager.common.validators import (
    InvalidPhoneNumberValidator,
    UniquePetNameValidator,
)
from mung_manager.customers.containers import CustomerContainer
from mung_manager.tickets.containers import TicketContainer


class CustomerListAPI(APIAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(BaseSerializer):
        customer_name = serializers.CharField(required=False, help_text="이름")
        customer_phone_number = serializers.CharField(required=False, help_text="고객 전화번호")
        customer_pet_name = serializers.CharField(required=False, help_text="반려동물 이름")
        is_active = serializers.BooleanField(required=True, help_text="활성화 여부")
        limit = serializers.IntegerField(
            default=10,
            min_value=1,
            max_value=50,
            help_text="페이지당 조회 개수",
        )
        offset = serializers.IntegerField(default=0, min_value=0, help_text="페이지 오프셋")

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField(label="고객 아이디")
        name = serializers.CharField(label="고객 이름")
        phone_number = serializers.CharField(label="고객 전화번호")
        customer_pets = inline_serializer(
            label="고객 반려동물 목록",
            source="undeleted_customer_pets",
            many=True,
            fields={
                "id": serializers.IntegerField(label="반려동물 아이디"),
                "name": serializers.CharField(label="반려동물 이름"),
            },
        )
        customer_tickets = inline_serializer(
            label="고객 티켓 목록",
            many=True,
            fields={
                "id": serializers.IntegerField(label="티켓 아이디"),
                "total_count": serializers.IntegerField(label="총 횟수"),
                "used_count": serializers.IntegerField(label="사용한 횟수"),
                "ticket": inline_serializer(
                    label="티켓 정보",
                    fields={
                        "ticket_type": serializers.CharField(label="티켓 타입"),
                        "usage_time": serializers.IntegerField(label="사용 가능한 시간"),
                    },
                ),
            },
        )
        memo = serializers.CharField(label="메모")
        recent_reserved_at = serializers.DateTimeField(label="최근 예약 일시")
        created_at = serializers.DateTimeField(label="생성 일시")
        is_active = serializers.BooleanField(label="활성화 여부")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pet_kindergarden_selector = CustomerContainer.pet_kindergarden_selector()
        self._customer_selector = CustomerContainer.customer_selector()

    def get(self, request: Request, pet_kindergarden_id: int) -> Response:
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        check_object_or_not_found(
            self._pet_kindergarden_selector.exists_by_id_and_user(
                pet_kindergarden_id=pet_kindergarden_id,
                user=request.user,
            ),
            msg=SYSTEM_CODE.message("NOT_FOUND_PET_KINDERGARDEN"),
            code=SYSTEM_CODE.code("NOT_FOUND_PET_KINDERGARDEN"),
        )
        customers = self._customer_selector.get_by_filter_for_search(filters=filter_serializer.validated_data)
        pagination_customers_data = get_paginated_data(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=customers,
            request=request,
            view=self,
        )
        return Response(data=pagination_customers_data, status=status.HTTP_200_OK)


class CustomerCreateAPI(APIAuthMixin, APIView):
    class InputSerializer(BaseSerializer):
        name = serializers.CharField(required=True, max_length=32, label="고객 이름")
        phone_number = serializers.CharField(
            required=True,
            min_length=11,
            max_length=16,
            validators=[InvalidPhoneNumberValidator()],
            label="고객 전화번호",
        )
        pets = serializers.ListField(
            child=serializers.CharField(),
            required=True,
            validators=[UniquePetNameValidator()],
            label="반려동물 이름 목록",
        )

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField(label="고객 아이디")
        name = serializers.CharField(label="고객 이름")
        phone_number = serializers.CharField(label="고객 전화번호")
        customer_pets = inline_serializer(
            label="고객 반려동물 목록",
            many=True,
            fields={
                "id": serializers.IntegerField(label="반려동물 아이디"),
                "name": serializers.CharField(label="반려동물 이름"),
            },
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._customer_service = CustomerContainer.customer_service()

    def post(self, request: Request, pet_kindergarden_id: int) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        customer = self._customer_service.create_customer(
            pet_kindergarden_id=pet_kindergarden_id,
            user=request.user,
            **input_serializer.validated_data,
        )
        customer_data = self.OutputSerializer(customer).data
        return Response(data=customer_data, status=status.HTTP_201_CREATED)


class CustomerBatchRegisterAPI(APIAuthMixin, APIView):
    class InputSerializer(BaseSerializer):
        csv_file = serializers.FileField(required=True, label="CSV 파일")

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField(label="고객 아이디")
        name = serializers.CharField(label="고객 이름")
        phone_number = serializers.CharField(label="고객 전화번호")
        customer_pets = inline_serializer(
            label="고객 반려동물 목록",
            many=True,
            fields={
                "id": serializers.IntegerField(label="반려동물 아이디"),
                "name": serializers.CharField(label="반려동물 이름"),
            },
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._customer_service = CustomerContainer.customer_service()

    def post(self, request: Request, pet_kindergarden_id: int) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        customers = self._customer_service.create_customers_by_csv(
            pet_kindergarden_id=pet_kindergarden_id,
            user=request.user,
            csv_file=input_serializer.validated_data["csv_file"],
        )
        customers_data = self.OutputSerializer(customers, many=True).data
        return Response(data=customers_data, status=status.HTTP_201_CREATED)


class CustomerDetailAPI(APIAuthMixin, APIView):
    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField(label="고객 아이디")
        name = serializers.CharField(label="고객 이름")
        phone_number = serializers.CharField(label="고객 전화번호")
        customer_pets = inline_serializer(
            label="고객 반려동물 목록",
            many=True,
            fields={
                "id": serializers.IntegerField(label="반려동물 아이디"),
                "name": serializers.CharField(label="반려동물 이름"),
            },
            source="undeleted_customer_pets",
        )
        memo = serializers.CharField(label="메모")
        created_at = serializers.DateTimeField(label="생성 일시")
        is_active = serializers.BooleanField(label="활성화 여부")
        is_kakao_user = serializers.SerializerMethodField(label="카카오 유저 여부")

        def get_is_kakao_user(self, obj) -> bool:
            return obj.user is None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pet_kindergarden_selector = CustomerContainer.pet_kindergarden_selector()
        self._customer_selector = CustomerContainer.customer_selector()

    def get(self, request: Request, pet_kindergarden_id: int, customer_id: int) -> Response:
        check_object_or_not_found(
            self._pet_kindergarden_selector.exists_by_id_and_user(
                pet_kindergarden_id=pet_kindergarden_id,
                user=request.user,
            ),
            msg=SYSTEM_CODE.message("NOT_FOUND_PET_KINDERGARDEN"),
            code=SYSTEM_CODE.code("NOT_FOUND_PET_KINDERGARDEN"),
        )
        customer = get_object_or_not_found(
            self._customer_selector.get_with_undeleted_customer_pet_by_id(
                customer_id=customer_id,
            ),
            msg=SYSTEM_CODE.message("NOT_FOUND_CUSTOMER"),
            code=SYSTEM_CODE.code("NOT_FOUND_CUSTOMER"),
        )
        customer_data = self.OutputSerializer(customer).data
        return Response(data=customer_data, status=status.HTTP_200_OK)


class CustomerToggleActiveAPI(APIAuthMixin, APIView):
    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField(label="고객 아이디")
        is_active = serializers.BooleanField(label="활성화 여부")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._customer_service = CustomerContainer.customer_service()

    def patch(self, request: Request, pet_kindergarden_id: int, customer_id: int) -> Response:
        customer = self._customer_service.toggle_customer_is_active(
            pet_kindergarden_id=pet_kindergarden_id,
            user=request.user,
            customer_id=customer_id,
        )
        customer_data = self.OutputSerializer(customer).data
        return Response(data=customer_data, status=status.HTTP_200_OK)


class CustomerUpdateAPI(APIAuthMixin, APIView):
    class InputSerializer(BaseSerializer):
        name = serializers.CharField(required=True, label="고객 이름")
        phone_number = serializers.CharField(
            required=True,
            label="고객 전화번호",
            validators=[InvalidPhoneNumberValidator()],
        )
        pets_to_add = serializers.ListField(
            child=serializers.CharField(),
            required=False,
            label="추가할 반려동물 이름 목록",
            validators=[UniquePetNameValidator()],
            default=[],
        )
        pets_to_delete = serializers.ListField(
            child=serializers.CharField(),
            required=False,
            label="삭제할 반려동물 이름 목록",
            validators=[UniquePetNameValidator()],
            default=[],
        )
        memo = serializers.CharField(required=False, allow_blank=True, label="메모")

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField(label="고객 아이디")
        name = serializers.CharField(label="고객 이름")
        phone_number = serializers.CharField(label="고객 전화번호")
        customer_pets = inline_serializer(
            label="고객 반려동물 목록",
            many=True,
            fields={
                "id": serializers.IntegerField(label="반려동물 아이디"),
                "name": serializers.CharField(label="반려동물 이름"),
            },
            source="undeleted_customer_pets",
        )
        memo = serializers.CharField(label="메모")
        created_at = serializers.DateTimeField(label="생성 일시")
        is_active = serializers.BooleanField(label="활성화 여부")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._customer_service = CustomerContainer.customer_service()

    def put(self, request: Request, pet_kindergarden_id: int, customer_id: int) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        customer = self._customer_service.update_customer(
            pet_kindergarden_id=pet_kindergarden_id,
            user=request.user,
            customer_id=customer_id,
            **input_serializer.validated_data,
        )
        customer_data = self.OutputSerializer(customer).data
        return Response(data=customer_data, status=status.HTTP_200_OK)


class CustomerTicketActiveListAPI(APIAuthMixin, APIView):
    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField(label="티켓 아이디")
        usage_time = serializers.IntegerField(label="사용 가능한 시간")
        usage_count = serializers.IntegerField(label="사용 가능한 횟수")
        usage_period_in_days_count = serializers.IntegerField(label="사용 가능 일수")
        price = serializers.IntegerField(label="가격")
        ticket_type = serializers.CharField(label="티켓 타입")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pet_kindergarden_selector = CustomerContainer.pet_kindergarden_selector()
        self._ticket_selector = TicketContainer.ticket_selector()

    def get(self, request: Request, pet_kindergarden_id: int) -> Response:
        check_object_or_not_found(
            self._pet_kindergarden_selector.exists_by_id_and_user(
                pet_kindergarden_id=pet_kindergarden_id,
                user=request.user,
            ),
            msg=SYSTEM_CODE.message("NOT_FOUND_PET_KINDERGARDEN"),
            code=SYSTEM_CODE.code("NOT_FOUND_PET_KINDERGARDEN"),
        )
        tickets = self._ticket_selector.get_querset_by_pet_kindergarden_id_for_undeleted_ticket(
            pet_kindergarden_id=pet_kindergarden_id,
        )
        tickets_data = self.OutputSerializer(tickets, many=True).data
        return Response(data=tickets_data, status=status.HTTP_200_OK)


class CustomerTicketListAPI(APIAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(BaseSerializer):
        limit = serializers.IntegerField(
            default=10,
            min_value=1,
            max_value=50,
            help_text="페이지당 조회 개수",
        )
        offset = serializers.IntegerField(default=0, min_value=0, help_text="페이지 오프셋")

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField(label="고객 티켓 등록 로그 아이디")
        usage_time = serializers.IntegerField(label="사용 가능한 시간", source="customer_ticket.ticket.usage_time")
        usage_count = serializers.IntegerField(label="사용 가능한 횟수", source="customer_ticket.ticket.usage_count")
        usage_period_in_days_count = serializers.IntegerField(
            label="사용 가능 일수", source="customer_ticket.ticket.usage_period_in_days_count"
        )
        price = serializers.IntegerField(label="가격", source="customer_ticket.ticket.price")
        ticket_type = serializers.CharField(label="티켓 타입", source="customer_ticket.ticket.ticket_type")
        created_at = serializers.DateTimeField(label="생성 일시")
        expired_at = serializers.DateTimeField(label="만료 일시", source="customer_ticket.expired_at")
        status = serializers.SerializerMethodField(label="상태")

        def get_status(self, obj) -> str:
            if obj.customer_ticket.expired_at < timezone.now():
                return "만료"
            return "이용중"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pet_kindergarden_selector = CustomerContainer.pet_kindergarden_selector()
        self._customer_selector = CustomerContainer.customer_selector()
        self._customer_ticket_registration_log_selector = CustomerContainer.customer_ticket_registration_log_selector()

    def get(self, request: Request, pet_kindergarden_id: int, customer_id: int) -> Response:
        check_object_or_not_found(
            self._pet_kindergarden_selector.exists_by_id_and_user(
                pet_kindergarden_id=pet_kindergarden_id,
                user=request.user,
            ),
            msg=SYSTEM_CODE.message("NOT_FOUND_PET_KINDERGARDEN"),
            code=SYSTEM_CODE.code("NOT_FOUND_PET_KINDERGARDEN"),
        )
        check_object_or_not_found(
            self._customer_selector.exists_by_id(customer_id=customer_id),
            msg=SYSTEM_CODE.message("NOT_FOUND_CUSTOMER"),
            code=SYSTEM_CODE.code("NOT_FOUND_CUSTOMER"),
        )
        customer_tickets = (
            self._customer_ticket_registration_log_selector.get_queryset_by_customer_id_for_ticket_registration_logs(
                customer_id=customer_id,
            )
        )
        pagination_customer_tickets_data = get_paginated_data(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=customer_tickets,
            request=request,
            view=self,
        )
        return Response(data=pagination_customer_tickets_data, status=status.HTTP_200_OK)


class CustomerTicketCreateAPI(APIAuthMixin, APIView):
    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField(label="티켓 아이디")
        total_count = serializers.IntegerField(label="총 사용 가능 횟수")
        used_count = serializers.IntegerField(label="사용한 횟수")
        expired_at = serializers.DateTimeField(label="만료 일시")
        created_at = serializers.DateTimeField(label="생성 일시")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._customer_ticket_service = CustomerContainer.customer_ticket_service()

    def post(
        self,
        request: Request,
        pet_kindergarden_id: int,
        customer_id: int,
        ticket_id: int,
    ) -> Response:
        customer_ticket = self._customer_ticket_service.register_ticket(
            customer_id=customer_id,
            pet_kindergarden_id=pet_kindergarden_id,
            user=request.user,
            ticket_id=ticket_id,
        )

        customer_ticket_data = self.OutputSerializer(customer_ticket).data
        return Response(data=customer_ticket_data, status=status.HTTP_201_CREATED)


class CustomerTicketLogListAPI(APIAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(BaseSerializer):
        limit = serializers.IntegerField(
            default=10,
            min_value=1,
            max_value=50,
            help_text="페이지당 조회 개수",
        )
        offset = serializers.IntegerField(default=0, min_value=0, help_text="페이지 오프셋")

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField(label="고객 티켓 사용 로그 아이디")
        ticket_type = serializers.CharField(label="티켓 타입", source="customer_ticket.ticket.ticket_type")
        usage_time = serializers.IntegerField(label="사용 가능한 시간", source="customer_ticket.ticket.usage_time")
        usage_count = serializers.IntegerField(label="사용 가능한 횟수", source="customer_ticket.ticket.usage_count")
        used_count = serializers.IntegerField(label="사용한 횟수")
        unused_count = serializers.IntegerField(label="잔여 횟수", source="customer_ticket.unused_count")
        is_attended = serializers.BooleanField(label="출석 여부", source="reservation.is_attended")
        reserved_at = serializers.DateTimeField(label="예약 일시", source="reservation.reserved_at")
        expired_at = serializers.DateTimeField(label="만료 일시", source="customer_ticket.expired_at")
        reservation_status = serializers.CharField(label="예약 상태", source="reservation.reservation_status")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pet_kindergarden_selector = CustomerContainer.pet_kindergarden_selector()
        self._customer_selector = CustomerContainer.customer_selector()
        self._customer_ticket_usage_log_selector = CustomerContainer.customer_ticket_usage_log_selector()

    def get(self, request: Request, pet_kindergarden_id: int, customer_id: int) -> Response:
        check_object_or_not_found(
            self._pet_kindergarden_selector.exists_by_id_and_user(
                pet_kindergarden_id=pet_kindergarden_id,
                user=request.user,
            ),
            msg=SYSTEM_CODE.message("NOT_FOUND_PET_KINDERGARDEN"),
            code=SYSTEM_CODE.code("NOT_FOUND_PET_KINDERGARDEN"),
        )
        check_object_or_not_found(
            self._customer_selector.exists_by_id(customer_id=customer_id),
            msg=SYSTEM_CODE.message("NOT_FOUND_CUSTOMER"),
            code=SYSTEM_CODE.code("NOT_FOUND_CUSTOMER"),
        )
        customer_ticket_usage_log = (
            self._customer_ticket_usage_log_selector.get_queryset_by_customer_id_for_ticket_usage_logs(
                customer_id=customer_id,
            )
        )
        pagination_customer_ticket_usage_log_data = get_paginated_data(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=customer_ticket_usage_log,
            request=request,
            view=self,
        )
        return Response(
            data=pagination_customer_ticket_usage_log_data,
            status=status.HTTP_200_OK,
        )
