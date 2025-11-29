from rest_framework import serializers
from .models import Credit


class CreditSerializer(serializers.ModelSerializer):
    loan_start_date = serializers.DateField(
        input_formats=['%d-%m-%Y', 'iso-8601'],
        help_text="Дата у форматі ДД-ММ-РРРР (наприклад, 10-01-2024)"
    )

    class Meta:
        model = Credit
        fields = (
            'id',
            'amount',
            'loan_start_date',
            'number_of_payments',
            'periodicity',
            'interest_rate'
        )
