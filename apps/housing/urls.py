from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r"housing", views.HousingViewSet, base_name="housing")
urlpatterns = router.urls
