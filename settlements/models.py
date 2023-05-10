from django.db import models

class Wallet(models.Model):
    # idk, i've considered the IBAN as an id, since it needs to be unique anyway, but can be changed
    id = models.CharField(max_length=50, primary_key=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Settlement(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    settlement_type = models.CharField(max_length=10)
    iban = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)
