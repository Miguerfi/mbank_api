from datetime import datetime
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from account.api.viewsets.serializers.account_serializer import AccountSerializer
from account.api.viewsets.serializers.card_serializer import CardSerializer
from account.api.viewsets.serializers.transaction_author_serializer import (
    TransactionAuthorSerializer,
)
from account.models import (
    Account,
    Balance,
    Card,
    TransactionAuthor,
    TransactionHistory,
    TransactionTarget,
)
from rest_framework.decorators import action
from rest_framework import status
import json
import random
import datetime
import string


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer = AccountSerializer
    authentication_classes = [TokenAuthentication]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset

        account_query = self.request.query_params.get("first_name", "")
        if account_query:
            queryset = queryset.filter(first_name__incontains=account_query)

        cpf_query = self.request.query_params.get("cpf", "")
        if account_query:
            queryset = queryset.filter(cpf__incontains=account_query)

        page = self.paginate_queryset(queryset)
        serializer = AccountSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        object = self.get_object()
        object.delete()
        object.save()
        return Response("deleted")

    def create(self, request, *args, **kwargs):
        user = Account()
        user.full_name = request.data["full_name"]
        user.nick = request.data["nick"]
        user.password = request.data["password"]
        user.email = request.data["email"]
        user.cpf = request.data["cpf"]
        user.birthdate = request.data["birthdate"]
        user.save()

        user_cpf = Account.objects.get(cpf=request.data["cpf"])
        balance = Balance.objects.create(cpf=user_cpf)

        ccard = Card.objects.create(cpf=user_cpf)

        user = Account.objects.get(nick=request.data["nick"])
        token = Token.objects.create(user=user)
        token_key = token.key
        token.user = user
        token.save()

        obj_token = {"token": token_key}
        return Response(obj_token, status=status.HTTP_201_CREATED)

    def generate_transaction_id(self):
        characters = string.ascii_letters + string.digits

        transaction_id = "".join(random.choices(characters, k=60))

        return transaction_id

    @action(methods=["post"], detail=False)
    def login(self, request, *args, **kwargs):
        cpf = request.data["cpf"]
        password = request.data["password"]
        auth = Account.objects.get(cpf=cpf, password=password)
        print(auth)

        response_content = {"Succes": "Logged"}
        return Response(response_content, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def saldo(self, request, *args, **kwargs):
        userId = request.user.id
        balance = Balance.objects.get(cpf=userId)
        saldo = balance.saldo
        dinheiro_guardado = balance.saved_money
        dinheiro_aplicado = balance.money_applied
        return JsonResponse(
            {
                "saldo": round(saldo, 2),
                "dinheiro_guardado": round(dinheiro_guardado, 2),
                "dinheiro_aplicado": round(dinheiro_aplicado, 2),
            }
        )

    @action(methods=["get"], detail=False)
    def me(self, request, *args, **kwargs):
        user_query = Account.objects.filter(id=request.user.id).values()
        serializer = AccountSerializer(user_query, many=True).data
        json_obj = json.dumps(serializer[0])

        data = json.loads(json_obj)
        return Response(data)

    @action(methods=["post"], detail=False)
    def create_card(self, request, *args, **kwargs):
        userId = request.user.id
        print(userId)
        card = Card.objects.get(cpf=userId)

        for i in range(1):
            ccnums = [random.randint(999, 9999) for _ in range(4)]
            conc_card_number = int("".join(map(str, ccnums)))
            card.card = conc_card_number

        ano = 2028
        rand_day = random.randint(1, 365)
        exp_date = datetime.datetime(ano, 1, 1) + datetime.timedelta(rand_day - 1)
        card.exp_data = exp_date

        for i in range(1):
            cvv = random.randint(99, 999)
            card.cvv = cvv

        card.save()

        content = {"Success": "Credit Card Created"}
        return Response(content, status=status.HTTP_201_CREATED)

    @action(methods=["get"], detail=False)
    def get_card_infos(self, request, *args, **kwargs):
        userId = Account.objects.get(id=request.user.id)
        card_query = Card.objects.filter(cpf_id=userId).values()
        serializer = CardSerializer(card_query, many=True).data

        json_obj = json.dumps(serializer[0])
        data = json.loads(json_obj)

        return Response(data, content_type="application/json")

    @action(methods=["post"], detail=False)
    def transaction_send(self, request, *args, **kwargs):
        user_submited = request.user
        user_target = request.data["target_user"]
        amount_send = request.data["amount_send"]
        generate_transaction = self.generate_transaction_id()

        get_target_id = Account.objects.get(email=user_target)
        balance_submited = Balance.objects.get(cpf=user_submited)
        balance_target = Balance.objects.get(cpf=get_target_id)

        if float(amount_send) > balance_submited.saldo:
            content_error = {"message": "saldo insuficiente"}
            return Response(content_error, status=status.HTTP_409_CONFLICT)
        else:
            balance_submited.saldo = balance_submited.saldo - float(amount_send)

            balance_target.saldo = float(amount_send) + balance_target.saldo
            balance_target.save()
            balance_submited.save()

        transaction = TransactionHistory()
        transaction.amount = amount_send
        if request.data["message"] != '':
            transaction.message = request.data["message"]
        transaction.transaction_id = generate_transaction
        transaction.save()

        filter_transactionID = TransactionHistory.objects.filter(
            transaction_id=generate_transaction
        ).first()
        get_author_transaction = Account.objects.get(id=request.user.id)

        transaction_author = TransactionAuthor()
        transaction_author.transaction_id = filter_transactionID
        transaction_author.author = get_author_transaction
        transaction_author.save()

        transaction_target = TransactionTarget()
        transaction_target.transaction_id = filter_transactionID
        transaction_target.target = get_target_id
        transaction_target.save()

        data = {
            "transaction_amount": transaction.amount,
            "transaction_message": transaction.message,
            "transaction_author": request.user.nick,
            "transaction_id": transaction.transaction_id,
        }
        return Response(data, status=status.HTTP_200_OK)
