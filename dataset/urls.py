from rest_framework.routers import DefaultRouter

from .views import DatasetModelViewSet, DataActionViewSet

router = DefaultRouter()
router.register(r'', DatasetModelViewSet, basename='datasets')
router.register(r'', DataActionViewSet, basename='data_action')

app_name = 'dataset'
urlpatterns = router.urls
