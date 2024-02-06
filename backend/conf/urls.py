from django.urls import (
    include,
    path,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from api.views import (
    ContactViewSet,
    LabelViewSet,
)
from apps.routers import CommonRouter

router = CommonRouter()

router.register(
    "contact",
    ContactViewSet,
)

router.register(
    "label",
    LabelViewSet,
)

urlpatterns = [
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name = "schema",
    ),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name = "swagger-ui",
    ),
    path(
        "",
        include(router.urls),
    )
]
