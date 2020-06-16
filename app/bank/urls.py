from rest_framework import routers

from app.bank.views import BankViewSet

router = routers.DefaultRouter()
router.register('v1/bank', BankViewSet)

urlpatterns = []

app_name = 'bank'
urlpatterns += router.urls
