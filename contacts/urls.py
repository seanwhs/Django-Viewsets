# contacts/urls.py
from rest_framework.routers import DefaultRouter
from .views import ModelViewSet

router = DefaultRouter()
router.register('contacts', ModelViewSet, basename='contacts')

urlpatterns = router.urls