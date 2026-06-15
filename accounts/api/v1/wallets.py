from rest_framework import viewsets
from accounts.models import Wallet
from accounts.api.v1.serializers import WalletSerializer
from rest_framework.permissions import IsAuthenticated


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]
