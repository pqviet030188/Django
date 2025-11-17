from django.db import models
from uuid import uuid4

# Create your models here.
def bill_thumbnail_upload_folder(instance, filename):
    uuid = f"{uuid4().hex}"
    return f"bill_thumbnails/{uuid}/{filename}"

class Bill(models.Model):

    STATUS_OPTIONS = [
        ('processing', 'Processing'),
        ('scheduled', 'Scheduled'),
        ('unable_to_pay', 'Unable to Pay'),
        ('paid', 'Paid'),
    ]

    STATUS_CONTEXTS = {
        'processing': "This bill is currently in processing, it can take approx. 1-2 hours depending on the time of day.",
        'scheduled': "This bill is scheduled to be paid and will be paid on the due date, you're in good hands!, etc.)",
        'unable_to_pay': "This bill can't be paid at the moment, please contact our support team for more information.",
        'paid': "This bill has been paid successfully, thank you for using Deferit!"
    }

    biller = models.CharField(max_length=1000)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_OPTIONS)
    status_context = models.TextField(blank=True)

    def update_status_context(self):
        self.status_context = self.STATUS_CONTEXTS.get(self.status, self.status_context)

    # call upon saving to update status context
    def save(self, *args, **kwargs):
        # update status context
        self.update_status_context()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Billing {self.biller} with {self.amount} on {self.date}"
    
class BillImage(models.Model):
    bill = models.ForeignKey(Bill, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=bill_thumbnail_upload_folder)
    
    def __str__(self):
        return f"Image for bill {self.bill.id}"