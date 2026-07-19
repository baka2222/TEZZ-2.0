from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.utils.functional import cached_property
from math import radians, sin, cos, sqrt, atan2


class ClientAd(models.Model):
    CHOISES_STATUS = [
        ('active', 'Активный'),
        ('inactive', 'Неактивный'),
    ]

    client = models.ForeignKey(
        'Client',
        verbose_name='Владелец объявления',
        on_delete=models.CASCADE,
        related_name='ads'
    )
    category_slug = models.CharField("Категория объявления", max_length=100)
    subcategory_slug = models.CharField("Подкатегория объявления", max_length=100)
    name = models.CharField("Название объявления", max_length=200)
    description = models.TextField("Описание", blank=True, default='')
    status_label = models.CharField(
        "Тип объявления (подпись)", max_length=100, blank=True, default=''
    )
    show_phone = models.BooleanField("Показывать телефон", default=False)
    price = models.IntegerField(
        "Цена",
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField("Валюта", max_length=10, default='KGS')

    channel_id = models.BigIntegerField("ID канала")
    message_id = models.BigIntegerField("ID сообщения")
    full_message_ids = models.JSONField("ID сообщений в канале", default=list, blank=True)

    status = models.CharField(
        "Статус объявления",
        max_length=20,
        choices=CHOISES_STATUS,
        default='active'
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Объявление клиента"
        verbose_name_plural = "Объявления клиентов"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.price} KGS ({self.get_status_display()})"


class Client(models.Model):
    LANGS = [
        ('ru', 'Русский'),
        ('kg', 'Кыргызский'),
        ('en', 'Английский'),
        ('cn', 'Китайский'),
    ]

    tg_code = models.CharField("Telegram ID", max_length=50, unique=True)
    name = models.CharField("Имя клиента", max_length=200, blank=True, null=True)
    phone = models.CharField("Номер телефона", max_length=30, blank=True, null=True)
    username = models.CharField("Юзернейм", max_length=150, blank=True, null=True)
    balance = models.DecimalField(
        verbose_name='Баланс (сом / тезики)',
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    language = models.CharField("Язык", max_length=2, choices=LANGS, default='ru')
    is_banned = models.BooleanField("Забанен", default=False)

    next_subscription_disable = models.DateTimeField(
        "Когда кончается безлимит", null=True, blank=True
    )
    next_ability = models.DateTimeField(
        "Когда можно будет снова публиковать", null=True, blank=True
    )
    next_ability_beauty = models.DateTimeField(
        "Когда можно будет снова публиковать BEAUTY", null=True, blank=True
    )
    next_ability_automoto = models.DateTimeField(
        "Когда можно будет снова публиковать AUTO/MOTO", null=True, blank=True
    )
    next_ability_housing = models.DateTimeField(
        "Когда можно будет снова публиковать HOUSING", null=True, blank=True
    )
    next_ability_techno = models.DateTimeField(
        "Когда можно будет снова публиковать TECHNO", null=True, blank=True
    )
    next_ability_job = models.DateTimeField(
        "Когда можно будет снова публиковать JOB", null=True, blank=True
    )

    favorites = models.ManyToManyField(
        ClientAd,
        verbose_name="Избранные объявления",
        related_name="favorited_by",
        blank=True,
    )

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name or self.tg_code
    

class TeziksTransaction(models.Model):
    sender = models.ForeignKey(
        Client,
        verbose_name="Отправитель",
        on_delete=models.SET_NULL,
        null=True,
        related_name='sent_transactions'
    )
    receiver = models.ForeignKey(
        Client,
        verbose_name="Получатель",
        on_delete=models.SET_NULL,
        null=True,
        related_name='received_transactions'
    )
    amount = models.DecimalField(
        verbose_name="Сумма",
        max_digits=10,
        decimal_places=2
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Транзакция тезиков"
        verbose_name_plural = "Транзакции тезиков"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.amount}"
