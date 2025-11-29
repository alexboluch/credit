from django.db import models
from django.core.validators import RegexValidator


class PeriodicityField(models.CharField):
    default_validators = [
        RegexValidator(
            r'^\d+[d|w|m|y]$',
            message="Формат періодичністі має бути: число + одиниця (d, w, m, y). Приклад: '30d'.",
            code='invalid_periodicity_format'
        )
    ]
