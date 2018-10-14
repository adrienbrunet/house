from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Housing
from .serializers import HousingSerializer


class HousingViewSet(viewsets.ModelViewSet):
    serializer_class = HousingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user_groups = self.request.user.profile.groups.all()
        return Housing.objects.filter(group__in=user_groups)
