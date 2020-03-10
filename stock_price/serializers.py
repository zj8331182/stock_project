from .models import StockPrice, StockFinance
from rest_framework import serializers


class PriceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StockPrice
        fields = ('number', 'open_price', 'close_price', 'high_price', 'low_price', 'date', 'volume')


class FinanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StockFinance
        fields = (
            'number', 'base_profit_pre_shares', 'net_assets_pre_shares', 'income_pre_shares', 'asset_liability_ratio',
            'date')
