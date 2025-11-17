from django.core.management.base import BaseCommand
from django.utils import timezone
from bills.models import Bill, Instalment , BillImage
from django.core.files import File
from uuid import uuid4
import random
import os
import calendar
import requests
from django.conf import settings
from datetime import datetime, timedelta


biller_names: list[str] = [
    "Mobile Co.",
    "Gas Co.",
    "Energy Co.",
    "Internet Co.",
    "Water Co.",
    "Council Co.",
    "Insurance Co.",
]

status_list: list[str] = [
    "processing",
    "scheduled",
    "paid",
    "unable_to_pay"
]

class Command(BaseCommand):
    help = 'Seed the database with sample Bills, Instalments, and Images'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding data...'))
        random.seed(42)
        year = 2024
        num_bills = 30
        bills = []

        folder = os.path.join(settings.MEDIA_ROOT, 'bill_thumbnails')
        os.makedirs(folder, exist_ok=True)

        filename = 'placeholder_500.jpg'
        filepath = os.path.join(folder, filename)
        relativepath = "/".join(["bill_thumbnails", filename])

        # Get placeholder data
        image_url = 'https://placehold.co/500/png'
        response = requests.get(image_url)
        response.raise_for_status() 

        with open(filepath, 'wb') as f:
            f.write(response.content)

        for bill_id in range(num_bills):
            month = random.randint(1, 12)
            day_of_month = calendar.monthrange(year, month)
            day = random.randint(1, day_of_month[1])
            bill_due = datetime.strptime(f"2024-{month:02}-{day:02}", "%Y-%m-%d")
            bill_amount = random.randint(100, 100000) / 100
            bill_status = random.choice(status_list)
            
            bill = Bill.objects.create(
                biller=random.choice(biller_names),
                amount=bill_amount,
                date=bill_due,
                status=bill_status
            )

            with open(filepath, 'rb') as f:
                image_file = File(f)
                BillImage.objects.create(
                    bill=bill,
                    image=relativepath
                )

            num_instalments = random.randint(5, 20)
            instalment_amount = bill_amount / num_instalments
            for x in range(num_instalments):
                Instalment.objects.create(
                    bill=bill,
                    amount=instalment_amount,
                    due=bill_due + timedelta(days=14 * x),
                    status='unpaid'
                )

        self.stdout.write(self.style.SUCCESS('Done!'))