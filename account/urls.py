from django.urls import path
from .api.viewsets import viewsets

urlpatterns = [
        path('',viewsets.AccountViewSet.create, name='create')
        ]
