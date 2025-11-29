from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Credit, Payment
from .serializers import CreditSerializer
from .utils import generate_payments, recalculate_payments


class CreditCreateView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer

    def perform_create(self, serializer):
        self.credit = serializer.save()
        self.payments = self.generate_payments(self.credit)

    def generate_payments(self, credit):
        payments_to_create = generate_payments(credit)
        return Payment.objects.bulk_create(payments_to_create)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        data = {
            'credit': serializer.data,
            'payments': [p.get_dict for p in self.payments]
        }
        return Response(
            data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ChangePaymentView(APIView):

    def post(self, request, *args, **kwargs):
        credit_id = request.data.get('id')
        payment_number = request.data.get('number')
        payment_sum = request.data.get('sum')

        if not all([credit_id, payment_number, payment_sum]):
            return Response(
                {"error": "Поля 'id', 'number' та 'sum' є обов'язковими."},
                status=status.HTTP_400_BAD_REQUEST
            )

        credit = Credit.objects.filter(id=credit_id).first()
        if not credit:
            return Response(
                {"error": f"Кредит з ID {credit_id} не знайдено."},
                status=status.HTTP_404_NOT_FOUND
            )
        payments = credit.payment_set.all()
        target_payment = payments.filter(id=payment_number).first()
        if not target_payment or payment_number == payments.count():
            return Response(
                {"error": f"Платіж з Number {payment_number} останній чи його не знайдено."},
                status=status.HTTP_404_NOT_FOUND
            )
        payments_to_update = recalculate_payments(credit, payments, payment_number, payment_sum)
        Payment.objects.bulk_update(payments_to_update, ['principal', 'interest', 'balance'])

        return Response({
            "data": {"payments": [p.get_dict for p in payments_to_update]},
            "status": "success",
            "message": "Success",
            "credit_id": credit_id
        }, status=status.HTTP_200_OK)