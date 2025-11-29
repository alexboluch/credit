from decimal import Decimal

from .models import Payment


def recalculate_payments(credit, payments, payment_number, payment_sum):
    N = credit.number_of_payments
    I = credit.interest_rate_per_period

    target_payment = payments.get(payment_number=payment_number)
    target_payment.principal = target_payment.principal - payment_sum
    payments_to_update = [target_payment]

    remaining_principal = target_payment.balance - target_payment.principal
    # ЕМІ = i*P / [1- (1+i)^-n]
    emi = I * remaining_principal / (1 - (1 + I) ** (-N + payment_number)) # коригуємо

    for i in range(payment_number + 1, N + 1):
        actual_principal = remaining_principal if i == N else emi

        payment = payments.get(payment_number=i)
        payment.principal = actual_principal
        payment.interest = remaining_principal * I
        payment.balance = remaining_principal

        payments_to_update.append(payment)
        remaining_principal -= actual_principal
    return payments_to_update


def generate_payments(credit):
    P = Decimal(credit.amount)
    N = credit.number_of_payments
    I = credit.interest_rate_per_period

    # ЕМІ = i*P / [1- (1+i)^-n]
    emi = I * P / (1 - (1 + I) ** -N)

    remaining_principal = P
    start_date = credit.loan_start_date
    payments_to_create = []
    for i in range(1, N + 1):
        payment_date = credit.calculate_next_payment_date(start_date)

        actual_principal = remaining_principal if i == N else emi

        payments_to_create.append(
            Payment(
                credit=credit,
                payment_number=i,
                date=payment_date,
                principal=actual_principal,
                interest=remaining_principal * I,
                balance=remaining_principal
            )
        )
        remaining_principal -= actual_principal
        start_date = payment_date
    return payments_to_create
