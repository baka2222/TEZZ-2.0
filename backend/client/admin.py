from django.contrib import admin
from .models import (
    Client,
    ClientAd,
    TeziksTransaction
)
from django import forms
from django.contrib import messages
from datetime import timedelta


LOCAL_TIME_FIELDS = [
    'next_ability',
    'next_ability_beauty',
    'next_ability_automoto',
    'next_ability_techno',
    'next_ability_housing',
    'next_ability_job',
    'next_subscription_disable',
]

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in LOCAL_TIME_FIELDS:
            val = getattr(self.instance, f, None)
            if val:
                self.initial[f] = val + timedelta(hours=6)
                self.fields[f].label = f"{self.fields[f].label} (Бишкек время)"
                self.fields[f].help_text = "Время по Бишкеку (UTC+6). При сохранении переведётся в UTC."

    def clean(self):
        cleaned = super().clean()
        for f in LOCAL_TIME_FIELDS:
            val = cleaned.get(f)
            if val:
                # Переводим Бишкек → UTC
                cleaned[f] = val - timedelta(hours=6)
        return cleaned


class ClientAdInline(admin.TabularInline):
    model = ClientAd
    extra = 0
    fields = (
        "name",
        "category_slug",
        "subcategory_slug",
        "price",
        "status",
        "show_phone",
        "channel_id",
        "message_id",
        "full_message_ids",
        "created_at_display",
    )
    readonly_fields = ("created_at_display",)
    show_change_link = False

    def created_at_display(self, obj):
        if obj.created_at:
            return (obj.created_at + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')
        return "—"

    created_at_display.short_description = "Создано (Бишкек)"


class FavoriteAdInline(admin.TabularInline):
    model = Client.favorites.through
    extra = 0
    verbose_name = "Избранное объявление"
    verbose_name_plural = "Избранные объявления"


class ClientAdmin(admin.ModelAdmin):
    form = ClientForm
    inlines = [ClientAdInline, FavoriteAdInline]

    list_display = (
        "name",
        "username",
        "phone",
        "tg_code",
        "balance",
        "is_banned",
        "language",
        "next_subscription_disable_display",
        "next_ability_display",
        "next_ability_beauty_display",
        "next_ability_automoto_display",
        "next_ability_techno_display",
        "next_ability_housing_display",
        "next_ability_job_display",
        "created_at_display",
        "updated_at_display",
    )
    search_fields = ("name", "username", "phone", "tg_code")
    list_filter = ("is_banned", "language", "created_at")
    list_editable = ("is_banned",)

    readonly_fields = (
        "created_at_display",
        "updated_at_display",
        "next_subscription_disable_display",
        "next_ability_display",
        "next_ability_beauty_display",
        "next_ability_automoto_display",
        "next_ability_techno_display",
        "next_ability_housing_display",
        "next_ability_job_display",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "username",
                    "phone",
                    "tg_code",
                    "balance",
                    "is_banned",
                    "language",
                    "next_ability",
                    "next_ability_beauty",
                    "next_ability_automoto",
                    "next_ability_techno",
                    "next_ability_housing",
                    "next_ability_job",
                    "next_subscription_disable",
                ),
            },
        ),
        (
            "Даты (Бишкек время)",
            {
                "fields": ("created_at_display", "updated_at_display"),
                "classes": ("collapse",),
            },
        ),
    )

    def created_at_display(self, obj):
        if obj.created_at:
            return (obj.created_at + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')
        return None
    created_at_display.short_description = "Создано (Бишкек)"

    def updated_at_display(self, obj):
        if obj.updated_at:
            return (obj.updated_at + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')
        return None
    updated_at_display.short_description = "Обновлено (Бишкек)"

    def next_ability_display(self, obj):
        if obj.next_ability:
            return (obj.next_ability + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')
        return None
    next_ability_display.short_description = "Веломаркет (Бишкек)"

    def next_ability_beauty_display(self, obj):
        if obj.next_ability_beauty:
            return (obj.next_ability_beauty + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')
        return None
    next_ability_beauty_display.short_description = "Бьютимаркет (Бишкек)"

    def next_ability_automoto_display(self, obj):
        if obj.next_ability_automoto:
            return (obj.next_ability_automoto + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')
        return None
    next_ability_automoto_display.short_description = "Автомотомаркет (Бишкек)"

    def next_ability_techno_display(self, obj):
        if obj.next_ability_techno:
            return (obj.next_ability_techno + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')
        return None
    next_ability_techno_display.short_description = "Техномаркет (Бишкек)"

    def next_ability_housing_display(self, obj):
        if obj.next_ability_housing:
            return (obj.next_ability_housing + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')
        return None
    next_ability_housing_display.short_description = "Недвижимость (Бишкек)"

    def next_ability_job_display(self, obj):
        if obj.next_ability_job:
            return (obj.next_ability_job + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')
        return None
    next_ability_job_display.short_description = "Работа (Бишкек)"

    def next_subscription_disable_display(self, obj):
        if obj.next_subscription_disable:
            return (obj.next_subscription_disable + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')
        return None
    next_subscription_disable_display.short_description = "Подписка (Бишкек)"


class TeziksTransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "amount", "created_at_display")
    search_fields = (
        "sender__name",
        "sender__phone",
        "sender__tg_code",
        "receiver__name",
        "receiver__phone",
        "receiver__tg_code",
    )
    list_filter = ("created_at",)
    autocomplete_fields = ("sender", "receiver")
    readonly_fields = ("created_at_display",)

    def created_at_display(self, obj):
        if obj.created_at:
            return (obj.created_at + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')
        return "—"

    created_at_display.short_description = "Создано (Бишкек)"


admin.site.register(Client, ClientAdmin)
admin.site.register(TeziksTransaction, TeziksTransactionAdmin)