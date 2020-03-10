import json

from django.core import serializers
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets

from .models import StockFinance, StockPrice
from .serializers import PriceSerializer, FinanceSerializer


def get_stocks_detail(param):
    return StockPrice.objects.filter(number=param).order_by("-date")


@require_http_methods(["GET"])
def list_stock_prices(request):
    response = {}
    print(request.GET.get('stock_number'))
    try:
        prices = get_stocks_detail(param=str(request.GET.get('stock_number')))
        paginator = Paginator(prices, 100)
        page = paginator.page(1)
        response['price_list'] = json.loads(serializers.serialize("json", prices))
        response['msg'] = 'success'
        response['error_code'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_code'] = 1
    return JsonResponse(response)


class PriceViewSet(viewsets.ModelViewSet):
    queryset = StockPrice.objects.all().order_by('date')
    serializer_class = PriceSerializer


class FinanceViewSet(viewsets.ModelViewSet):
    queryset = StockFinance.objects.all().order_by('date')
    serializer_class = FinanceSerializer
