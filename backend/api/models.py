"""
django orm 모델을 정의합니다.
"""
from django.core.validators import RegexValidator
from django.db import models

phone_number_regex = RegexValidator(
    regex = r"^(0[1-9]{1}[0-9]{0,1})-(\d{3,4})-(\d{4})$",
)

class Contact(models.Model):
    """
    연락처 정보를 담는 ORM 모델입니다.
    """
    contact_id = models.AutoField(
        primary_key = True,
        help_text = "연락처 id",
    )

    profile = models.URLField(
        max_length = 2083,
        null = True,
        help_text = "프로필 사진 url",
    )

    name = models.CharField(
        max_length = 100,
        help_text = "이름",
    )

    email = models.EmailField(
        null = True,
        help_text = "이메일",
    )

    phone = models.CharField(
        max_length = 100,
        validators = [ phone_number_regex ],
        help_text = "전화번호",
    )

    company = models.CharField(
        max_length = 100,
        null = True,
        help_text = "회사",
    )

    position = models.CharField(
        max_length = 100,
        null = True,
        help_text = "직책",
    )

    memo = models.TextField(
        null = True,
        help_text = "메모",
    )

    address = models.TextField(
        null = True,
        help_text = "주소",
    )

    birthday = models.DateField(
        null = True,
        help_text = "생일",
    )

    website = models.URLField(
        max_length = 2083,
        null = True,
        help_text = "웹사이트",
    )

    labels = models.ManyToManyField(
        "Label",
        related_name = "contact",
        db_column = "label",
        through = "ContactLabel",
        help_text = "연결된 라벨",
    )

    class Meta:
        db_table = "tb_contact"

        constraints = [
            models.UniqueConstraint(
                fields = ["phone"],
                name = "ix_api_contact_01",
            ),
        ]

        indexes = [
            models.Index(
                fields = ["name"],
                name = "ix_api_contact_02",
            ),
            models.Index(
                fields = ["email"],
                name = "ix_api_contact_03",
            ),
            models.Index(
                fields = ["phone"],
                name = "ix_api_contact_04",
            ),
        ]


class Label(models.Model):
    """
    라벨 정보를 담는 ORM 모델입니다.
    """
    label_id = models.AutoField(
        primary_key = True,
        help_text = "라벨 id",
    )

    label_name = models.CharField(
        max_length = 100,
        help_text = "라벨 이름",
    )

    class Meta:
        db_table = "tb_label"


class ContactLabel(models.Model):
    """
    연락처와 라벨 정보를 매개하는 ORM 모델입니다.
    """
    contact = models.ForeignKey(
        Contact,
        on_delete = models.CASCADE,
        db_column = "contact_id",
        help_text = "연락처 id",
    )

    label = models.ForeignKey(
        Label,
        on_delete = models.CASCADE,
        db_column = "label_id",
        help_text = "라벨 id",
    )

    class Meta:
        db_table = "tb_contact_label"
