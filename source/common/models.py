from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractDatetimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Время создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Время изменения'))

    class Meta:
        abstract = True


class AbstractCreatedByModel(AbstractDatetimeModel):
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Кем создано'),
    )

    class Meta:
        abstract = True