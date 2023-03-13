from datetime import datetime
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import account
from account.api.viewsets.serializers.account_serializer import AccountSerializer
from account.models import Account
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
import json

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
        print("aqui")
        user.birthdate = request.data["birthdate"]
        user.save()
        user = Account.objects.get(nick=request.data["nick"])

        token = Token.objects.create(user=user)
        token_key = token.key
        token.user = user
        token.save()

        obj_token = {
                'token':token_key
                }
        return Response(obj_token, status=status.HTTP_201_CREATED)

    @action(methods=["post"], detail=False)
    def login(self, request, *args, **kwargs):
        cpf = request.data["cpf"]
        password = request.data["password"]
        auth = Account.objects.get(cpf=cpf, password=password)
        print(auth)

        response_content = {
                "Succes":"Logged"
                }
        return Response(response_content,status=status.HTTP_200_OK)

    @action(methods=["get"],detail=False)
    def saldo(self, request,*args,**kwargs):
        saldo = request.user.saldo
        return JsonResponse({'saldo':saldo})

    @action(methods=["get"],detail=False)
    def me(self,request,*args,**kwargs):
        nick = request.user.nick
        return JsonResponse({'nick':nick})
