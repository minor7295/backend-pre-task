"""
앱을 프로젝트에 등록할 때에 사용합니다.
"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    name = "api"
