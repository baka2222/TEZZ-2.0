# yourapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Lesson, Mark

@receiver(post_save, sender=Lesson)
def create_marks_for_lesson_students(sender, instance, created, **kwargs):
    """
    По созданию урока создаём Mark для всех студентов связанного класса.
    Используем transaction.on_commit — чтобы гарантировать, что Lesson уже сохранён.
    """
    if not created:
        return

    # получаем студентов из связанного класса
    students_qs = instance.module.school_class.students.all()

    def _create_marks():
        for student in students_qs:
            # get_or_create — чтобы избежать дубликатов при повторном вызове
            Mark.objects.get_or_create(
                lesson=instance,
                student=student,
                defaults={'score': None, 'answer': None}
            )

    # выполняем после коммита (безопаснее, если вызывается в транзакции)
    transaction.on_commit(_create_marks)
