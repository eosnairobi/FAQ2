from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from .api.views import CategoryModelViewSet, ToolModelViewSet
from .views import filter, render_tools, tools, map

router = DefaultRouter()


router.register(r'api-tools', ToolModelViewSet, base_name='api-tools')
router.register(r'api-categories', CategoryModelViewSet,
                base_name='api-categories')

urlpatterns = [
    path('', tools, name='tools'),
    path('map/', map, name='map'),
    path('render-tools/', render_tools, name='all_tools'),
    re_path(r'^tool/(?P<category_id>[\w-]+)/$', filter, name='filter'),
]
urlpatterns += router.urls
