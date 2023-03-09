from rest_framework.serializers import ModelSerializer
from account.models import Card


class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ("card", "cvv", "exp_data", "cpf")
