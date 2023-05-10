from django.db import models

class Transfer(models.Model):
    from_iban = models.CharField(max_length=50)
    to_iban = models.CharField(max_length=50)
    # let's say for more they need assistance, so the bank isn't that shitty in the end
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=(
        ('initiated', 'Initiated'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ), default='initiated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: Transfer from {} to {} ({})'.format(self.created_at, self.from_iban, self.to_iban, self.amount)
