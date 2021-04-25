from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractDatetimeModel


class Deal(AbstractDatetimeModel):
    customer = models.CharField(
        max_length=100,
        verbose_name=_("Клиент"),
    )
    item = models.CharField(
        max_length=100,
        verbose_name=_("Предмет"),
    )
    total = models.IntegerField(
        validators=[MinValueValidator(0), ],
        verbose_name=_("Потраченная сумма"),

    )
    qty = models.IntegerField(
        validators=[MinValueValidator(0), ],
        verbose_name=_("Количество"),

    )
    date_time = models.DateTimeField(
        verbose_name=_("Дата"),
    )
    request_number = models.IntegerField(
        validators=[MinValueValidator(0), ],
        verbose_name=_("Номер запроса")
    )

    class Meta:
        verbose_name = _('Сделка')
        verbose_name_plural = _('Сделки')
