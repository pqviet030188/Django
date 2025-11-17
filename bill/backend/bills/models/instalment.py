from django.db import models
from uuid import uuid4
from . import Bill

class Instalment(models.Model):
    STATUS_OPTIONS = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]

    bill = models.ForeignKey(Bill, related_name='instalments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_OPTIONS)

    def __str__(self):
        return f"Instalment for {self.bill.biller} on {self.due} with {self.status}"