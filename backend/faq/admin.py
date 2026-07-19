from django.contrib import admin

from .models import FAQCategory, FAQItem


class FAQItemInline(admin.StackedInline):
    model = FAQItem
    extra = 0
    fields = (
        "order",
        "is_active",
        ("question", "question_en"),
        ("question_kg", "question_cn"),
        "answer",
        "answer_en",
        "answer_kg",
        "answer_cn",
    )
    show_change_link = True


class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "app_type", "emoji", "items_count", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("app_type", "is_active")
    search_fields = ("name", "name_en", "name_kg", "name_cn")
    inlines = [FAQItemInline]
    fieldsets = (
        (None, {"fields": ("app_type", "emoji", "order", "is_active")}),
        ("Название", {"fields": ("name", "name_en", "name_kg", "name_cn")}),
    )

    def items_count(self, obj):
        return obj.items.count()

    items_count.short_description = "Вопросов"


class FAQItemAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("question", "question_en", "question_kg", "question_cn")
    fieldsets = (
        (None, {"fields": ("category", "order", "is_active")}),
        ("Вопрос", {"fields": ("question", "question_en", "question_kg", "question_cn")}),
        ("Ответ", {"fields": ("answer", "answer_en", "answer_kg", "answer_cn")}),
    )


admin.site.register(FAQCategory, FAQCategoryAdmin)
admin.site.register(FAQItem, FAQItemAdmin)
