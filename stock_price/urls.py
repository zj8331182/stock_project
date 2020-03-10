from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'list_stock_prices$', views.list_stock_prices),
]
