from django.urls import path
from rest_framework.routers import DefaultRouter

from .api.views import CategoryModelViewSet, ToolModelViewSet

router = DefaultRouter()


router.register(r'api-tools', ToolModelViewSet, base_name='api-tools')
router.register(r'api-categories', CategoryModelViewSet,
                base_name='api-categories')

urlpatterns = [
    # path()
]
urlpatterns += router.urls
