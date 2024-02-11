"""
django orm과 json의 상호변환을 담당합니다.
"""
from django.db import IntegrityError

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import (
    Contact,
    Label,
)

class LabelCreateSerializer(serializers.ModelSerializer):
    """
    라벨 생성시 사용하는 serializer입니다.
    """
    class Meta:
        model = Label
        fields = ["label_name"]


class LabelListSerializer(serializers.ModelSerializer):
    """
    라벨 목록 조회시 사용하는 serializer입니다.
    """
    class Meta:
        model = Label
        fields = "__all__"


class LabelUpdateSerializer(serializers.ModelSerializer):
    """
    라벨 수정시 사용하는 serializer입니다.
    """
    class Meta:
        model = Label
        fields = "__all__"


class ContactListSerializer(serializers.ModelSerializer):
    """
    연락처 목록 조회시 사용하는 serializer입니다.
    """
    company_position = serializers.CharField(
        read_only = True,
        help_text = "회사 (직책)",
    )

    labels = LabelListSerializer(
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

class ContactDetailSerializer(serializers.ModelSerializer):
    """
    연락처 상세 정보 조회시 사용하는 serializer입니다.
    """
    labels = LabelListSerializer(
        many=True,
        read_only=True,
    )

    def create(self, validated_data):
        try:
            super().create(validated_data)
        except IntegrityError as e:
            raise ValidationError(
                f"'{validated_data['phone']}'는 이미 등록된 전화번호입니다.",
            ) from e

    class Meta:
        model = Contact
        fields = "__all__"
