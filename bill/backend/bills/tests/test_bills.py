from urllib.parse import urlencode
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.test import Client
from ..models import Bill, BillImage
from ..views import get_bill, get_bills

@override_settings(ROOT_URLCONF='bills.urls')
class BillEndpointTests(TestCase):

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
            ),
            Bill.objects.create(
                biller="User 3",
                amount=400.00,
                date=timezone.now().date(),
                status='unable_to_pay',
            ),
            Bill.objects.create(
                biller="User 4",
                amount=500.00,
                date=timezone.now().date(),
                status='paid',
            ),
        ]

        [cls.scheduled, cls.processing, cls.unable_to_pay, cls.paid] = cls.bills

        cls.firstBillImages = [
            BillImage.objects.create(bill=cls.scheduled, image="test")
        ]
        
        cls.client = Client()

    def test_get_bill(self):
        # setup
        bill = self.scheduled
        url = reverse(get_bill, args=[bill.id])
        
        # act
        response = self.client.get(url)
        data = response.json()

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], bill.id, "Does not receive correct bill from id")
        self.assertEqual(data['images'][0]['image'], "/media/test", "Expect correct image url")

    def test_get_bill_not_found(self):
        # setup
        max_id = max([bill.id for bill in self.bills])
        url = reverse(get_bill, args=[max_id + 10])
        
        # act
        response = self.client.get(url)
        data = response.json()

        # assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'Not found', "Bill cannot be found")

    def test_get_all_bills_with_empty_cursor(self):
        # setup
        url = reverse(get_bills)
        query_params = urlencode({'limit': 2})
        url = f"{url}?{query_params}"

        # act
        response = self.client.get(url)
        data = response.json()

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(data['results']), 2, "Result length must be less than 2")
        self.assertEqual(data['results'][0]['id'], self.scheduled.id, "First bill id must be the expected value")
        self.assertEqual(data['results'][0]['images'][0]['image'], "/media/test", "First bill image must be the expected value")
        self.assertEqual(data['results'][1]['id'], self.processing.id, "Second bill id must be the expected value")

    def test_get_all_bills_with_empty_limit(self):
        # setup
        url = reverse(get_bills)

        # act
        response = self.client.get(url)
        data = response.json()

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(data['results']), 10, "Result length must be less than 10")
        self.assertEqual(data['results'][0]['id'], self.scheduled.id, "First bill id must be the expected value")
        self.assertEqual(data['results'][1]['id'], self.processing.id, "Second bill id must be the expected value")

    def test_get_all_bills_with_non_empty_cursor_and_limit(self):
        # setup
        processing_bill = self.processing
        url = reverse(get_bills)
        query_params = urlencode({'limit': 2, 'cursor': processing_bill.id})
        url = f"{url}?{query_params}"

        # act
        response = self.client.get(url)
        data = response.json()

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(data['results']), 2, "Result length must be less than 2")
        self.assertEqual(data['results'][0]['id'], self.unable_to_pay.id, "First bill id must be the expected value")
        self.assertEqual(data['results'][1]['id'], self.paid.id, "Second bill id must be the expected value")