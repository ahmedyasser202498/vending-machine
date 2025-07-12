from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProductViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('products', ProductViewSet)

urlpatterns = router.urls
