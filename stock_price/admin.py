from django.contrib import admin
from .models import StockFinance, StockPrice

# Register your models here.
admin.site.register(StockFinance)
admin.site.register(StockPrice)
