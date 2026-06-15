import logging
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, exceptions
from accounts.models import Wallet
from accounts.api.v1.serializers import WalletSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle


class WalletViewSet(viewsets.GenericViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Wallet.objects.get(user=self.request.user)

    def throttled(self, request, wait):
        logger = logging.getLogger("api_request")
        logger.error(f"Rate limit exceeded for user {request.user.username}: {wait}")
        raise exceptions.Throttled(wait)

    @action(detail=False, methods=["GET"])
    def details(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"], throttle_classes=[UserRateThrottle])
    def deposit(self, request):
        wallet = Wallet.objects.select_for_update().filter(user=request.user).first()
        serializer = self.get_serializer(wallet, data=request.data)
        serializer.is_valid(raise_exception=True)
        wallet.deposit(serializer.validated_data["balance"])
        return Response(serializer.data)

    @action(detail=False, methods=["POST"], throttle_classes=[UserRateThrottle])
    def withdraw(self, request):
        wallet = Wallet.objects.select_for_update().filter(user=request.user).first()
        serializer = self.get_serializer(wallet, data=request.data)
        serializer.is_valid(raise_exception=True)
        wallet.withdraw(serializer.validated_data["balance"])
        return Response(serializer.data)
