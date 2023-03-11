from datetime import datetime
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

class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer = AccountSerializer

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
        account = Account()
        account.full_name = request.data['full_name']
        account.cpf = request.data['cpf']
        account.nick = request.data['nick']
        account.password = request.data['password']
        account.birthdate = request.data['birthdate']
        account.last_login = datetime.now()
        account.date_joined = datetime.now()
        account.save()
        response_content = "Account Created"
        return Response(response_content,status=status.HTTP_201_CREATED)

    @action(methods=['post'],detail=False)
    def login(self,request,*args,**kwargs):
        cpf = request.data['cpf']
        password = request.data['password']
        auth = Account.objects.get(cpf=cpf,password=password)
        print(auth)
        return Response("OK")
