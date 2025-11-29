from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal

from .models import Credit, Payment


class CreditCreationTestCase(APITestCase):

    def test_valid_data(self):
        data = {
            "amount": 1000,
            "loan_start_date": "10-01-2024",
            "number_of_payments": 4,
            "periodicity": "3w",
            "interest_rate": 0.1,
        }
        response = self.client.post('/api/credits/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Credit.objects.count(), 1)
        self.assertEqual(Payment.objects.count(), 4)

        response_data = response.data
        valid_credit_data = {
            'amount': '1000.00',
            'loan_start_date': '2024-01-10',
            'number_of_payments': 4,
            'periodicity': '3w',
            'interest_rate': '0.10'
        }
        for key in valid_credit_data.keys():
            self.assertEqual(response_data['credit'][key], valid_credit_data[key])

        old_principal_number = Payment.objects.get(payment_number=2).principal

        response = self.client.post('/api/change_payment/', {'id': 1, 'number': 2, 'sum': 100}, format='json')

        new_payments = list(Payment.objects.filter(credit_id=1).values('payment_number', 'principal', 'interest', 'balance'))
        self.assertEqual(old_principal_number - 100, new_payments[1]['principal'])
        self.assertEqual(new_payments[2],
            {'payment_number': 3, 'principal': Decimal('298.95'), 'interest': Decimal('3.42'), 'balance': Decimal('592.76')}
        )
        self.assertEqual(new_payments[3],
            {'payment_number': 4, 'principal': Decimal('293.81'), 'interest': Decimal('1.70'), 'balance': Decimal('293.81')}
        )
        self.assertEqual(Payment.objects.count(), 4)


    def test_invalid_data(self):
        invalid_data = {
            "amount": -1000,
            "loan_start_date": "10-01-blabla",
            "periodicity": "3w",
            "interest_rate": 0.1,
        }
        response = self.client.post('/api/credits/', invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Credit.objects.count(), 0)
        self.assertEqual(response.data['loan_start_date'][0].code, 'invalid')
        self.assertEqual(response.data['number_of_payments'][0].code, 'required')

        response = self.client.post('/api/change_payment/', {'id': 1, 'number': 2, 'sum': 100}, format='json')
        self.assertIn('error', response.data)
