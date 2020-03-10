from django.db import models


class StockPrice(models.Model):
    number = models.TextField()
    open_price = models.TextField()
    close_price = models.TextField()
    high_price = models.TextField()
    low_price = models.TextField()
    date = models.TextField()
    volume = models.TextField()

    def __str__(self):
        return self.number + "-" + self.date


class StockFinance(models.Model):
    number = models.TextField()
    base_profit_pre_shares = models.TextField(null=True)
    net_assets_pre_shares = models.TextField(null=True)
    income_pre_shares = models.TextField(null=True)
    asset_liability_ratio = models.TextField(null=True)
    date = models.TextField()

    def __str__(self):
        return self.number + "-" + self.date
