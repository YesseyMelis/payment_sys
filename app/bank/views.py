from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from app.bank.models import Application
from app.bank.serializers import ApplicationCreateSerializer


class BankViewSet(viewsets.GenericViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializer

    @action(
        methods=['post'], detail=False,
    )
    def apply(self, request):
        ser = self.get_serializer(data=request.query_params)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response("Заявка одобрена", status=status.HTTP_200_OK)
