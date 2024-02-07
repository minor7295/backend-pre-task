from django.db import transaction
from django.db.models import (
    F,
    Value,
)
from django.db.models.functions import Concat

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiExample,
)

from rest_framework import (
    mixins,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import (
    Contact,
    ContactLabel,
    Label,
)
from api.serializers import (
    ContactDetailSerializer,
    ContactListSerializer,
    LabelCreateSerializer,
    LabelUpdateSerializer,
    LabelListSerializer,
    )

@extend_schema_view(
    create = extend_schema(description = "### 주소록 등록 \n\n"),
    destroy = extend_schema(description = "### 주소록 삭제 \n\n"),
    list = extend_schema(
        description = \
            "### 연락처 목록 (주소록) 조회 \n\n" \
            "cursor 파라미터 기반으로 페이지네이션이 적용되어있습니다. \n\n" \
            "응답에서 next/previous에 적힌 url로 이후/이전 페이지의" \
            "데이터를 조회할 수 있습니다. \n\n" \
            "또한 ordering 파라미터 기반으로 정렬된 응답을 받을 수 있습니다. \n\n" \
            "name, email, phone 중 하나의 필드를 선택하여 전달하면 " \
            "해당 필드 기준으로 오름차순/내림차순으로 정렬된 응답을 받을 수 있습니다. \n\n" \
            "예를 들어 name을 전달하면 이름 기준 오름차순, -name을 전달하면 이름 기준 내림차순" \
            "으로 정렬된 응답을 받을 수 있습니다.",
        examples = [
            OpenApiExample(
                "연락처 정보",
                value = {
                    "next": "http://localhost/contact/?cursor=cD01",
                    "previous": None,
                    "results": [
                        {
                            "contact_id": 1,
                            "profile": "https://www.gstatic.com/identity/boq/profilepicturepicker/photo_silhouette_e02a5f5deb3ffc173119a01bc9575490.png",
                            "name": "강건우",
                            "email": "yunseo28@example.com",
                            "phone": "055-386-9875",
                            "company_position": "(주) 장이윤 (도장공)",
                            "labels": [{"label_id": 1, "label_name": "Lime"}],
                        },
                    ],
                },
            ),
        ],
    ),
    retrieve = extend_schema(description = "### 주소록 조회 \n\n"),
    update = extend_schema(description = "### 주소록 수정 \n\n"),
    label = extend_schema(
        description = \
            "### 라벨 적용 \n\n" \
            "contact_id로 특정한 연락처에 라벨을 적용합니다.\n\n" \
            "기존에 등록되었던 라벨은 모두 삭제되고, " \
            "요청으로 명시한 라벨의 정보만 남게 됩니다. \n\n" \
    ),
)
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact \
        .objects \
        .all() \
        .prefetch_related("labels")

    serializer_class = ContactDetailSerializer

    ordering  = "contact_id"

    ordering_fields = [
        "name",
        "email",
        "phone",
    ]

    def get_serializer_class(self):
        if self.action == "label":
            return LabelListSerializer
        elif self.action == "list":
            return ContactListSerializer
        else:
            return ContactDetailSerializer

    def filter_queryset(self, queryset):
        queryset = super() \
            .filter_queryset(queryset) \
            .annotate(
                company_position = Concat(
                    F("company"),
                    Value(" ("),
                    F("position"),
                    Value(")"),
                ),
            )

        return queryset

    @action(detail=True, methods=["PUT"])
    def label(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        with transaction.atomic():
            contact = self.get_object()
            ContactLabel.objects.filter(contact_id=contact).delete()
            for d in data:
                ContactLabel(
                    contact_id=contact.contact_id,
                    label_id = d["label_id"],
                    ).save()
        serializer = LabelListSerializer(
            data = data,
            many = True,
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

@extend_schema_view(
    create = extend_schema(description = "### 라벨 등록 \n\n"),
    destroy = extend_schema(description = "### 라벨 삭제 \n\n"),
    list = extend_schema(description = "### 라벨 목록 조회 \n\n"),
    update = extend_schema(description = "### 라벨 이름 수정 \n\n"),
)
class LabelViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Label.objects.all()

    serializer_class = LabelListSerializer

    pagination_class = None

    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.action == "create":
            return LabelCreateSerializer
        elif self.action == "update":
            return LabelUpdateSerializer
        else:
            return super().get_serializer_class()
