from rest_framework.serializers import ModelSerializer
from account.models import TransactionAuthor


class TransactionAuthorSerializer(ModelSerializer):
    class Meta:
        model = TransactionAuthor
        fields = "__all__" 
