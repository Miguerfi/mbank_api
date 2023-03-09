from rest_framework.viewsets import ModelViewSet
from account.api.viewsets.serializers.account_serializer import AccountSerializer
from account.models import Account
from rest_framework.decorators import action


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer = AccountSerializer

    @action(methods=['post'],detail=False)
    def create_account(self, request):
        full_name = request.data['full_name']
        conta = Account
        
