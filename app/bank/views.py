from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from payment_sys.app.bank.models import Application
from payment_sys.app.bank.serializers import ApplicationCreateSerializer


class BankViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializer

    @action(
        method=['post'],
        detail=False
    )
    def apply(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response("Заявка одобрена", status=status.HTTP_200_OK)
