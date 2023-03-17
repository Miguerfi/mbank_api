from rest_framework.serializers import ModelSerializer
from account.models import TransactionTarget


class TransactionTargetSerializer(ModelSerializer):
    class Meta:
        model = TransactionTarget
        fields = "__all__"
