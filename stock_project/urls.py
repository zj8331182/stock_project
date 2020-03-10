"""stock_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers

import stock_price.urls
from stock_price import views
from . import view as main_views

router = routers.DefaultRouter()
router.register(r'prices', views.PriceViewSet)
router.register(r'finance', views.FinanceViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'api/', include(stock_price.urls)),
    url(r'task/copyPrice', main_views.copy_prices),
    url(r'task/syncPrice', main_views.sync_price),
    path(r'', TemplateView.as_view(template_name='index.html')),
    url('', include(router.urls)),
]
