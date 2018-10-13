from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r"addresses", views.AddressViewSet, base_name="address")
urlpatterns = router.urls
