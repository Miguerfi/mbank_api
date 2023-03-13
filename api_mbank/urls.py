"""api_mbank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from account.api.viewsets.viewsets import AccountViewSet
urlpatterns = [
    path("admin/", admin.site.urls),
    path("createaccount/",AccountViewSet.as_view({'post':'create'})),
    path("login/",AccountViewSet.as_view({'post':'login'})),
    path('saldo/',AccountViewSet.as_view({'get':'saldo'})),
    path('me/',AccountViewSet.as_view({'get':'me'}))
]
