from django.db import models
from django.utils.functional import cached_property
from dateutil.relativedelta import relativedelta
from decimal import Decimal

from .fields import PeriodicityField


class Credit(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    loan_start_date = models.DateField()
    number_of_payments = models.PositiveIntegerField()
    periodicity = PeriodicityField(max_length=5)
    interest_rate = models.DecimalField(decimal_places=2, max_digits=5)
    create_date = models.DateTimeField(auto_now_add=True)

    PERIODICITY_TYPES = {
        'd': 'days',
        'w': 'weeks',
        'm': 'months',
    }

    PERIOD_LENGTH = {
        'days': 1,
        'weeks': 52,
        'months': 12
    }

    @cached_property
    def periodicity_number(self):
        return int(self.periodicity[:-1])

    @cached_property
    def periodicity_type(self):
        return self.PERIODICITY_TYPES.get(self.periodicity[-1])

    def calculate_next_payment_date(self, start_date):
        return start_date + relativedelta(**{self.periodicity_type: self.periodicity_number})

    def calculate_next_year_rate(self, start_date, payment_date):
        return (payment_date - start_date).days / 365

    @cached_property
    def period_length(self):
        return Decimal(self.periodicity_number / self.PERIOD_LENGTH.get(self.periodicity_type))

    @cached_property
    def interest_rate_per_period(self):
        return Decimal(self.period_length * self.interest_rate)


class Payment(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE)
    payment_number = models.PositiveIntegerField()
    date = models.DateField()
    principal = models.DecimalField(decimal_places=2, max_digits=10)
    interest = models.DecimalField(decimal_places=2, max_digits=10)
    balance = models.DecimalField(decimal_places=2, max_digits=10)

    @cached_property
    def payment(self):
        return self.principal + self.interest

    @cached_property
    def get_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'principal': self.principal,
            'interest': self.interest
        }
