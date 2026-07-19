from django.db import models


class Payment(models.Model):
    """
    Подтверждённый платёж (пополнение баланса).

    Пишется ботом только после успешного приёма чека — либо автоматически
    по OCR, либо вручную админом. Фотографии чеков НЕ хранятся: чтобы не
    раздувать БД, оставляем только распознанные метаданные.
    """

    class Method(models.TextChoices):
        OCR = 'ocr', 'OCR (авто)'
        ADMIN = 'admin', 'Админ (вручную)'

    client = models.ForeignKey(
        'client.Client',
        verbose_name='Клиент',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
    )
    tg_code = models.CharField('Telegram ID', max_length=50, blank=True, default='')
    username = models.CharField('Юзернейм', max_length=150, blank=True, default='')
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
    method = models.CharField(
        'Как принято', max_length=10, choices=Method.choices
    )
    transaction_id = models.CharField(
        'ID транзакции (из чека)', max_length=100,
        blank=True, default='', db_index=True,
        help_text='Используется для защиты от повторной отправки одного чека.'
    )
    ocr_confidence = models.FloatField(
        'Уверенность OCR, %', null=True, blank=True
    )
    receipt_datetime = models.DateTimeField(
        'Дата/время на чеке', null=True, blank=True
    )
    created_at = models.DateTimeField('Принято', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.amount} — {self.get_method_display()} — {self.tg_code}'
