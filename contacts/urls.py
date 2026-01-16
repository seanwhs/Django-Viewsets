# contacts/urls.py
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet  

router = DefaultRouter()
router.register('contacts', ContactViewSet, basename='contacts')  # Fixed reference
urlpatterns = router.urls
