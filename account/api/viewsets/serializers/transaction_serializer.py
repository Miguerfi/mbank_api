from rest_framework.serializers import ModelSerializer
from account.models import TransactionHistory


class TransactionHistorySerializer(ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = "__all__"
