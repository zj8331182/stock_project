from django.http import HttpResponse
from stock_price import tasks


def copy_prices(request):
    res = tasks.copy_database.delay()
    return HttpResponse("Hello world ! " + str(res))


def sync_price(request):
    year = request.GET.get('year')
    index = request.GET.get('index')
    res = tasks.sync_price.delay(year, index)
    return HttpResponse("Hello world ! " + str(res))
