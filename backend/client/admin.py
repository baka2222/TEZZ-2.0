from django.contrib import admin
from .models import (
    Client,
    Shop,
    Product,
    Service,
    Order,
    OrderItem,
    PricingRule,
    TimeSurcharge,
    CourierOrder,
    ProductImage,
)
from client.models import Category
from django.contrib import messages
from django import forms
from datetime import timedelta

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "name_en", "name_kg", "name_cn", "description")

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = (
        "name",
        "name_en",
        "name_kg",
        "name_cn",
        "price",
        "description",
        "description_en",
        "description_kg",
        "description_cn",
    )
    show_change_link = True

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0
    fields = (
        "name",
        "name_en",
        "name_kg",
        "name_cn",
        "price",
        "description",
        "description_en",
        "description_kg",
        "description_cn",
    )
    show_change_link = True

class ShopAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "address",
        "created_at_display",
        "category",
        "point_a_lat",
        "point_a_lng",
    )
    search_fields = ("name", "owner__name", "owner__phone")
    autocomplete_fields = ("owner",)
    list_filter = ("owner", "category", "created_at")
    readonly_fields = ("created_at_display",)
    inlines = [ProductInline, ServiceInline]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "category",
                    "owner",
                    "address",
                    "description",
                    "description_en",
                    "description_kg",
                    "description_cn",
                    "point_a_lat",
                    "point_a_lng",
                ),
            },
        ),
        (
            "Дополнительно",
            {"fields": ("created_at_display",), "classes": ("collapse",)},
        ),
    )

    def created_at_display(self, obj):
        return (obj.created_at + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')

    created_at_display.short_description = "Создано"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner__phone=str(request.user.last_name))

from django import forms
from django.contrib import admin
from django.contrib import messages
from datetime import timedelta
from .models import Client  # убедись, что импорт правильный

# Список полей с таймерами, которые нужно переводить в UTC+6
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
        # При загрузке формы переводим UTC → Бишкек для отображения
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


class ClientAdmin(admin.ModelAdmin):
    form = ClientForm

    # Поля, отображаемые в списке (с местным временем через display-методы)
    list_display = (
        "name",
        "username",
        "phone",
        "tg_code",
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

    # Поля только для чтения (display-методы)
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

    # Группировка полей в форме редактирования
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "username",
                    "phone",
                    "tg_code",
                    "is_banned",
                    "language",
                    # Редактируемые поля (оригинальные, форма сама переведёт время)
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

    # ---------- Display-методы для показа местного времени (UTC+6) ----------
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

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    fields = ("image_url",)
    show_change_link = False

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "shop", "price", "created_at_display")
    search_fields = ("name", "name_en", "name_kg", "name_cn", "shop__name")
    list_filter = ("shop", "created_at")
    readonly_fields = ("created_at_display",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "name_en",
                    "name_kg",
                    "name_cn",
                    "price",
                    "description",
                    "description_en",
                    "description_kg",
                    "description_cn",
                ),
            },
        ),
        (
            "Дополнительно",
            {"fields": ("created_at_display",), "classes": ("collapse",)},
        ),
    )
    exclude = ("shop",)
    inlines = [ProductImageInline,]

    def created_at_display(self, obj):
        return (obj.created_at + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')

    created_at_display.short_description = "Создано"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(shop__owner__phone=str(request.user.last_name))

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            try:
                client = Client.objects.get(phone=str(request.user.last_name))
                shop = Shop.objects.get(owner=client)
                obj.shop = shop
            except Client.DoesNotExist:
                self.message_user(
                    request, "Клиент с таким телефоном не найден.", level=messages.ERROR
                )
                return
            except Shop.DoesNotExist:
                self.message_user(
                    request, "У этого клиента нет магазина.", level=messages.ERROR
                )
                return
        elif not request.user.is_superuser:
            if obj.shop.owner.phone != str(request.user.last_name):
                self.message_user(
                    request,
                    "Вы не можете редактировать товары чужого магазина.",
                    level=messages.ERROR,
                )
                return
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            return readonly_fields + ("shop",)
        return readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if "shop" in form.base_fields:
                form.base_fields["shop"].widget = forms.HiddenInput()
                form.base_fields["shop"].required = False
        return form

class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "shop", "price", "created_at_display")
    search_fields = ("name", "name_en", "name_kg", "name_cn", "shop__name")
    list_filter = ("shop", "created_at")
    readonly_fields = ("created_at_display",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "name_en",
                    "name_kg",
                    "name_cn",
                    "price",
                    "description",
                    "description_en",
                    "description_kg",
                    "description_cn",
                ),
            },
        ),
        (
            "Дополнительно",
            {"fields": ("created_at_display",), "classes": ("collapse",)},
        ),
    )
    exclude = ("shop",)

    def created_at_display(self, obj):
        return (obj.created_at + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')

    created_at_display.short_description = "Создано"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(shop__owner__phone=str(request.user.last_name))

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            try:
                client = Client.objects.get(phone=str(request.user.last_name))
                shop = Shop.objects.get(owner=client)
                obj.shop = shop
            except Client.DoesNotExist:
                self.message_user(
                    request, "Клиент с таким телефоном не найден.", level=messages.ERROR
                )
                return
            except Shop.DoesNotExist:
                self.message_user(
                    request, "У этого клиента нет магазина.", level=messages.ERROR
                )
                return
        elif not request.user.is_superuser:
            if obj.shop.owner.phone != str(request.user.last_name):
                self.message_user(
                    request,
                    "Вы не можете редактировать услуги чужого магазина.",
                    level=messages.ERROR,
                )
                return
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            return readonly_fields + ("shop",)
        return readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if "shop" in form.base_fields:
                form.base_fields["shop"].widget = forms.HiddenInput()
                form.base_fields["shop"].required = False
        return form

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ("product", "service", "quantity")
    show_change_link = False

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "shop", "client", "total_price", "created_at_display")
    search_fields = ("shop__name", "client__name", "client__phone")
    list_filter = ("shop", "client", "created_at")
    readonly_fields = ("total_price", "created_at_display")
    fieldsets = (
        (None, {"fields": ("shop", "client")}),
        (
            "Дополнительно",
            {"fields": ("total_price", "created_at_display"), "classes": ("collapse",)},
        ),
    )
    inlines = [OrderItemInline]

    def created_at_display(self, obj):
        return (obj.created_at + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')

    created_at_display.short_description = "Создано"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(shop__owner__phone=str(request.user.last_name))

class PricingRuleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "min_distance",
        "max_distance",
        "base_price",
        "per_km_price",
        "multiplier",
    )
    list_editable = (
        "min_distance",
        "max_distance",
        "base_price",
        "per_km_price",
        "multiplier",
    )
    ordering = ("min_distance",)
    search_fields = ("name",)

class TimeSurchargeAdmin(admin.ModelAdmin):
    list_display = ("name", "start_time", "end_time", "multiplier")
    ordering = ("start_time",)
    search_fields = ("name",)

class CourierOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client",
        "courier",
        "distance_km",
        "price",
        "status",
        "created_at_display",
    )
    list_filter = ("courier", "status", "created_at")
    search_fields = (
        "client__name",
        "client__phone",
        "courier__name",
        "courier__phone",
        "comment",
    )
    readonly_fields = (
        "distance_km",
        "price",
        "created_at_display",
        "updated_at_display",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "client",
                    "courier",
                    "point_a_lat",
                    "point_a_lng",
                    "point_b_lat",
                    "point_b_lng",
                    "comment",
                    "status",
                ),
            },
        ),
        (
            "Результаты расчётов",
            {
                "fields": (
                    "distance_km",
                    "price",
                    "created_at_display",
                    "updated_at_display",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def created_at_display(self, obj):
        return (obj.created_at + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')

    created_at_display.short_description = "Создано"

    def updated_at_display(self, obj):
        return (obj.updated_at + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')

    updated_at_display.short_description = "Обновлено"

admin.site.register(Category, CategoryAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(PricingRule, PricingRuleAdmin)
admin.site.register(TimeSurcharge, TimeSurchargeAdmin)
admin.site.register(CourierOrder, CourierOrderAdmin)