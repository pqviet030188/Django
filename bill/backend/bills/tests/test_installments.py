from urllib.parse import urlencode
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.test import Client

from ..models import Instalment, Bill
from ..views import get_instalments, get_all_bill_instalments

@override_settings(ROOT_URLCONF='bills.urls')
class InstalmentEndpointTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.bills = [
            Bill.objects.create(
                biller="User 1",
                amount=200.00,
                date=timezone.now().date(),
                status='scheduled',
            ),
            Bill.objects.create(
                biller="User 2",
                amount=300.00,
                date=timezone.now().date(),
                status='processing',
            )
        ]

        cls.bill = cls.bills[0]

        cls.instalments = [
            Instalment.objects.create(
                bill=cls.bill,
                due=timezone.now().date(),
                status='unpaid',
                amount = 10
            ),
            Instalment.objects.create(
                bill=cls.bill,
                due=timezone.now().date(),
                status='unpaid',
                amount = 20
            ),
            Instalment.objects.create(
                bill=cls.bill,
                due=timezone.now().date(),
                status='unpaid',
                amount = 30
            ),
            Instalment.objects.create(
                bill=cls.bill,
                due=timezone.now().date(),
                status='unpaid',
                amount = 40
            ),
            Instalment.objects.create(
                bill=cls.bill,
                due=timezone.now().date(),
                status='unpaid',
                amount = 50
            ),
            Instalment.objects.create(
                bill=cls.bill,
                due=timezone.now().date(),
                status='unpaid',
                amount = 60
            ),
            Instalment.objects.create(
                bill=cls.bill,
                due=timezone.now().date(),
                status='unpaid',
                amount = 70
            ),
            Instalment.objects.create(
                bill=cls.bill,
                due=timezone.now().date(),
                status='unpaid',
                amount = 80
            ),
            Instalment.objects.create(
                bill=cls.bill,
                due=timezone.now().date(),
                status='unpaid',
                amount = 90
            ),
            Instalment.objects.create(
                bill=cls.bill,
                due=timezone.now().date(),
                status='unpaid',
                amount = 100
            ),
            Instalment.objects.create(
                bill=cls.bill,
                due=timezone.now().date(),
                status='unpaid',
                amount = 110
            ),
        ]

        cls.client = Client()

    def test_get_instalments(self):
        # setup
        bill = self.bill
        url = reverse(get_instalments, args=[bill.id])
        
        # act
        response = self.client.get(url)
        data = response.json()
        
        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['results']) <= 10, True, "Result length must be less than 10")

        # shallow comparison
        self.assertEqual(
        [
            rec['id'] for rec in data['results']
        ], 
        [
            rec.id for rec in self.instalments[:10]
        ], "Must be the expected instalments")

        self.assertEqual(data['next_cursor'], self.instalments[9:][0].id, "Next cursor must be the expected value")

    def test_get_instalments_with_empty_cursor(self):
        # setup
        bill = self.bill
        url = reverse(get_instalments, args=[bill.id])
        query_params = urlencode({'limit': 2})
        url = f"{url}?{query_params}"
        
        # act
        response = self.client.get(url)
        data = response.json()
        
        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['results']), 2, "Result length must be 2")

        # shallow comparison
        self.assertEqual(
        [
            rec['id'] for rec in data['results']
        ], 
        [
            rec.id for rec in self.instalments[:2]
        ], "Must be the expected instalments")

        self.assertEqual(data['next_cursor'], self.instalments[1:][0].id, "Next cursor must be the expected value")

    def test_get_instalments_with_empty_limit(self):
        # setup
        bill = self.bill
        url = reverse(get_instalments, args=[bill.id])
        query_params = urlencode({'cursor': 2})
        url = f"{url}?{query_params}"
        
        # act
        response = self.client.get(url)
        data = response.json()
        
        # assert
        instalments = [instalment for instalment in self.instalments if instalment.id > 2]
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(data['results']), 10, "Result length must be at max 10")

        # shallow comparison
        self.assertEqual(
        [
            rec['id'] for rec in data['results']
        ], 
        [
            rec.id for rec in instalments[:10]
        ], "Must be the expected instalments")

        self.assertEqual(data['next_cursor'], 
                        instalments[-1].id if instalments[-1] is not None else None, "Next cursor must be the expected value")

    def test_get_instalments_with_empty_return(self):
        # setup
        bill = self.bill
        url = reverse(get_instalments, args=[bill.id + 1000])
        
        # act
        response = self.client.get(url)
        data = response.json()
        
        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['results']), 0, "Result length must be 0")
        self.assertEqual(data['next_cursor'], None, "Next cursor must be empty")

    def test_get_all_instalments(self):
        # setup
        bill = self.bill
        url = reverse(get_all_bill_instalments, args=[bill.id])
        
        # act
        response = self.client.get(url)
        data = response.json()
        
        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['results']), len(self.instalments), "Result must be the expected value")