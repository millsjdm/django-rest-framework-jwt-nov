
# Third-Party
from rest_framework import routers

# Local
from .views import UserViewSet
from .views import RoleViewSet

router = routers.DefaultRouter(
    trailing_slash=False,
)

router.register(r'role', RoleViewSet)
router.register(r'user', UserViewSet)
urlpatterns = router.urls
