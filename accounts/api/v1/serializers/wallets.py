from rest_framework import serializers
from accounts.models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    user = serializers.CurrentUserDefault()
    class Meta:
        model = Wallet
        fields = ["user", "balance"]
        read_only_fields = ["user"]
