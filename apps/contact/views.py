from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import ContactSerializer


class ContactView(CreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
