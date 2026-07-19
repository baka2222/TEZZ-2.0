from django.db import models


class FAQCategory(models.Model):
    APP_CHOICES = [
        ('market_bot', 'TEZZ Market Bot'),
    ]

    app_type = models.CharField(
        "Тип", max_length=30, choices=APP_CHOICES, default='market_bot'
    )
    name = models.CharField("Название (рус)", max_length=100)
    name_en = models.CharField("Название (англ)", max_length=100, blank=True, default='')
    name_kg = models.CharField("Название (кырг)", max_length=100, blank=True, default='')
    name_cn = models.CharField("Название (кит)", max_length=100, blank=True, default='')
    emoji = models.CharField("Эмодзи", max_length=8, blank=True, default='')
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активна", default=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Категория FAQ"
        verbose_name_plural = "FAQ · Категории"
        ordering = ["app_type", "order", "id"]

    def __str__(self):
        return f"{self.get_app_type_display()} — {self.name}"


class FAQItem(models.Model):
    category = models.ForeignKey(
        FAQCategory,
        verbose_name="Категория",
        on_delete=models.CASCADE,
        related_name="items"
    )
    question = models.CharField("Вопрос (рус)", max_length=255)
    question_en = models.CharField("Вопрос (англ)", max_length=255, blank=True, default='')
    question_kg = models.CharField("Вопрос (кырг)", max_length=255, blank=True, default='')
    question_cn = models.CharField("Вопрос (кит)", max_length=255, blank=True, default='')
    answer = models.TextField("Ответ (рус)")
    answer_en = models.TextField("Ответ (англ)", blank=True, default='')
    answer_kg = models.TextField("Ответ (кырг)", blank=True, default='')
    answer_cn = models.TextField("Ответ (кит)", blank=True, default='')
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Вопрос-ответ"
        verbose_name_plural = "FAQ · Вопросы-ответы"
        ordering = ["category", "order", "id"]

    def __str__(self):
        return self.question[:60]
