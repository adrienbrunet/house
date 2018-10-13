from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Address
from .serializers import AddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.profile.addresses.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile)

    @action(methods=["patch"], detail=True)
    def set_as_primary(self, request, pk=None):
        address = self.get_object()
        address.set_as_primary()
        return Response(AddressSerializer(address).data)
