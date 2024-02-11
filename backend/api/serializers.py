from rest_framework import serializers

from api.models import (
    Contact,
    Label,
)

class LabelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ["label_name"]


class LabelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = "__all__"


class LabelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = "__all__"


class ContactListSerializer(serializers.ModelSerializer):
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
    labels = LabelListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Contact
        fields = "__all__"
