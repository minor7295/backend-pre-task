from drf_spectacular.utils import (
    extend_schema_serializer,
    OpenApiExample,
)
from rest_framework import serializers

from api.models import (
    Contact,
    Label,
)

@extend_schema_serializer(
    examples = [
        OpenApiExample(
            "라벨 정보",
            value = {"label_id": 1, "label_name": "Lime"},
        ),
    ],
)
class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = "__all__"


@extend_schema_serializer(
    examples = [
        OpenApiExample(
            "연락처 목록 정보",
            value = {
                "contact_id" : 1,
                "profile" : "https://www.gstatic.com/identity/boq/profilepicturepicker/photo_silhouette_e02a5f5deb3ffc173119a01bc9575490.png",
                "name" : "강건우",
                "email" : "yunseo28@example.com",
                "phone" : "055-386-9875",
                "company_position" : "주 장이윤 도장공",
                "labels": [{"label_id": 1, "label_name": "Lime"}],
            },
        ),
    ],
)
class ContactListSerializer(serializers.ModelSerializer):
    company_position = serializers.CharField(
        read_only = True,
        help_text = "회사 (직책)",
    )

    labels = LabelSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Contact
        fields = [
            "contact_id",
            "profile",
            "name",
            "email",
            "phone",
            "company_position",
            "labels",
        ]


@extend_schema_serializer(
    examples = [
        OpenApiExample(
            "연락처 등록 요청",
            value = {
                "profile" : "https://www.gstatic.com/identity/boq/profilepicturepicker/photo_silhouette_e02a5f5deb3ffc173119a01bc9575490.png",
                "name" : "강건우",
                "email" : "yunseo28@example.com",
                "phone" : "055-386-9875",
                "company" : "(주) 장이윤",
                "position" : "도장공",
                "memo" : "Voluptatem eveniet",
                "address" : "경기도 증평군 봉은사536가",
                "birthday" : "2001-10-03",
                "website" : "https://www.imgim.net/",
            },
            request_only = True,
        ),
        OpenApiExample(
            "연락처 수정 요청",
            value = {
                "contact_id" : 1,
                "profile" : "https://www.gstatic.com/identity/boq/profilepicturepicker/photo_silhouette_e02a5f5deb3ffc173119a01bc9575490.png",
                "name" : "강건우",
                "email" : "yunseo28@example.com",
                "phone" : "055-386-9875",
                "company" : "(주) 장이윤",
                "position" : "도장공",
                "memo" : "Voluptatem eveniet",
                "address" : "경기도 증평군 봉은사536가",
                "birthday" : "2001-10-03",
                "website" : "https://www.imgim.net/",
            },
            request_only = True,
        ),
        OpenApiExample(
            "연락처 상세 정보",
            value = {
                "contact_id" : 1,
                "profile" : "https://www.gstatic.com/identity/boq/profilepicturepicker/photo_silhouette_e02a5f5deb3ffc173119a01bc9575490.png",
                "name" : "강건우",
                "email" : "yunseo28@example.com",
                "phone" : "055-386-9875",
                "company" : "(주) 장이윤",
                "position" : "도장공",
                "memo" : "Voluptatem eveniet",
                "address" : "경기도 증평군 봉은사536가",
                "birthday" : "2001-10-03",
                "website" : "https://www.imgim.net/",
                "labels" : [{"label_id": 1, "label_name": "Lime"}],
            },
            response_only = True,
        ),
    ],
)
class ContactDetailSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Contact
        fields = "__all__"
