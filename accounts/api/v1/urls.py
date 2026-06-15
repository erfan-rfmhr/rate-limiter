from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"wallets", views.WalletViewSet, basename="wallets")
urlpatterns = router.urls
