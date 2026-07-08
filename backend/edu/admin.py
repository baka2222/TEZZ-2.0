from django.contrib import admin
from .models import Class, Module, Lesson, Mark
from django.contrib.auth import get_user_model
from datetime import timedelta
User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "role", "email", "is_active", 'telegram', 'discord', "is_staff", "is_superuser", "last_login_display", "date_joined_display")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("id",)
    list_editable = ("role", "is_active")
    fieldsets = (
        ("Основная информация", {
            "fields": ("username", "first_name", "last_name", "email", "password")
        }),
        ("Роль и доступ", {
            "fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Даты", {
            "fields": ("last_login_display", "date_joined_display")
        }),
    )
    readonly_fields = ("last_login_display", "date_joined_display")

    def last_login_display(self, obj):
        if obj.last_login:
            return (obj.last_login + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')
        return None
    last_login_display.short_description = "Последний вход"

    def date_joined_display(self, obj):
        return (obj.date_joined + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')
    date_joined_display.short_description = "Дата регистрации"


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    show_change_link = True


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "teacher", "is_active", "created_at_display")
    list_filter = ("is_active", "teacher")
    search_fields = ("name", "teacher__first_name", "teacher__last_name")
    ordering = ("name",)
    inlines = [ModuleInline]
    filter_horizontal = ("students",)
    list_editable = ("is_active",)

    def created_at_display(self, obj):
        return (obj.created_at + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')
    created_at_display.short_description = "Создано"


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    show_change_link = True


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "school_class", "created_at_display")  # <-- изменено
    list_filter = ("school_class",)  # <-- изменено
    search_fields = ("title", "school_class__name")  # <-- изменено
    ordering = ("title",)
    inlines = [LessonInline]

    def created_at_display(self, obj):
        return (obj.created_at + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')
    created_at_display.short_description = "Создано"


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "module", "created_at_display", "start_time", "end_time")
    list_filter = ("module",)
    search_fields = ("title", "module__title")
    ordering = ("title",)

    def created_at_display(self, obj):
        return (obj.created_at + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')
    created_at_display.short_description = "Создано"


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "lesson", "score", "created_at_display")
    list_filter = ("lesson", "student", "score")
    search_fields = ("student__first_name", "student__last_name", "lesson__title")
    ordering = ("-created_at",)
    list_editable = ("score",)

    def created_at_display(self, obj):
        return (obj.created_at + timedelta(hours=6)).strftime('%d.%m.%Y %H:%M:%S')
    created_at_display.short_description = "Создано"
