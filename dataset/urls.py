from rest_framework.routers import DefaultRouter

from .views import DatasetModelViewSet

router = DefaultRouter()
router.register(r'', DatasetModelViewSet, basename='datasets')

app_name = 'dataset'
urlpatterns = router.urls
