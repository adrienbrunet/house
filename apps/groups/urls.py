from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r"groups", views.GroupViewSet, base_name="group")
urlpatterns = router.urls
