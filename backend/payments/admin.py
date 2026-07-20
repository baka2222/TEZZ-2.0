import base64
import io
from datetime import timedelta

from django import forms
from django.contrib import admin
from django.db.models import Sum, Count, DateTimeField, ExpressionWrapper, F
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html

from .models import Payment


BISHKEK_SHIFT = timedelta(hours=6)


def _range_totals(qs):
    agg = qs.aggregate(total=Sum('amount'), cnt=Count('id'))
    return agg['total'] or 0, agg['cnt'] or 0


def _bishkek_today_start():
    """Начало текущих суток по Бишкеку (UTC+6), возвращается в UTC."""
    now_local = timezone.now() + BISHKEK_SHIFT
    local_midnight = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    return local_midnight - BISHKEK_SHIFT


class PaymentForm(forms.ModelForm):
    """created_at в форме — по Бишкеку (UTC+6), в БД уходит в UTC."""

    class Meta:
        model = Payment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        f = self.fields['created_at']
        f.label = f'{f.label} (Бишкек время)'
        f.help_text = 'Время по Бишкеку (UTC+6). При сохранении переведётся в UTC.'
        val = getattr(self.instance, 'created_at', None)
        if val:
            self.initial['created_at'] = val + BISHKEK_SHIFT
        else:
            self.initial['created_at'] = timezone.now() + BISHKEK_SHIFT

    def clean_created_at(self):
        val = self.cleaned_data.get('created_at')
        # Бишкек → UTC
        return val - BISHKEK_SHIFT if val else val


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    form = PaymentForm
    list_display = (
        'created_at_display', 'amount', 'method_badge', 'client_col',
        'tg_code', 'transaction_id', 'ocr_confidence', 'receipt_datetime_display',
    )
    list_filter = ('method', 'created_at')
    search_fields = ('tg_code', 'username', 'transaction_id', 'client__name')
    date_hierarchy = 'created_at'
    list_per_page = 50
    actions = ['export_selected_excel']
    change_list_template = 'admin/payments/payment_changelist.html'

    # ---------- Колонки списка ----------

    @admin.display(description='Принято (Бишкек)', ordering='created_at')
    def created_at_display(self, obj):
        if obj.created_at:
            return (obj.created_at + BISHKEK_SHIFT).strftime('%d.%m.%Y %H:%M:%S')
        return '—'

    @admin.display(description='Дата чека (Бишкек)', ordering='receipt_datetime')
    def receipt_datetime_display(self, obj):
        # receipt_datetime парсится напрямую с текста чека (receipt_ocr.py) —
        # там уже местное бишкекское время, сдвигать повторно не нужно
        if obj.receipt_datetime:
            return obj.receipt_datetime.strftime('%d.%m.%Y %H:%M:%S')
        return '—'

    @admin.display(description='Как принято', ordering='method')
    def method_badge(self, obj):
        color = '#2e7d32' if obj.method == Payment.Method.OCR else '#1565c0'
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;'
            'border-radius:10px;font-size:11px;">{}</span>',
            color, obj.get_method_display(),
        )

    @admin.display(description='Клиент')
    def client_col(self, obj):
        if obj.client:
            return obj.client.name or obj.client.tg_code
        return obj.username or obj.tg_code or '—'

    # ---------- Сводка над списком ----------

    def _summary(self):
        today_start = _bishkek_today_start()
        week_start = today_start - timedelta(days=7)
        month_start = today_start - timedelta(days=30)

        today_sum, today_cnt = _range_totals(
            Payment.objects.filter(created_at__gte=today_start))
        week_sum, week_cnt = _range_totals(
            Payment.objects.filter(created_at__gte=week_start))
        month_sum, month_cnt = _range_totals(
            Payment.objects.filter(created_at__gte=month_start))

        by_method = {
            row['method']: row['c']
            for row in Payment.objects.filter(created_at__gte=month_start)
            .values('method').annotate(c=Count('id'))
        }
        return {
            'today_sum': today_sum, 'today_cnt': today_cnt,
            'week_sum': week_sum, 'week_cnt': week_cnt,
            'month_sum': month_sum, 'month_cnt': month_cnt,
            'ocr_cnt': by_method.get('ocr', 0),
            'admin_cnt': by_method.get('admin', 0),
            'report_url': reverse('admin:payments_report'),
            'excel_url': reverse('admin:payments_export_excel'),
        }

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(self._summary())
        return super().changelist_view(request, extra_context)

    # ---------- Кастомные URL: отчёт с графиком + Excel ----------

    def get_urls(self):
        custom = [
            path('report/', self.admin_site.admin_view(self.report_view),
                 name='payments_report'),
            path('export-excel/', self.admin_site.admin_view(self.export_excel),
                 name='payments_export_excel'),
        ]
        return custom + super().get_urls()

    def _daily_chart(self, days: int) -> str:
        """PNG-график сумм по дням за N дней -> base64 data-uri (matplotlib Agg)."""
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        today = _bishkek_today_start()
        start = today - timedelta(days=days - 1)

        rows = (
            Payment.objects.filter(created_at__gte=start)
            .annotate(local_dt=ExpressionWrapper(
                F('created_at') + BISHKEK_SHIFT, output_field=DateTimeField()))
            .annotate(d=TruncDate('local_dt'))
            .values('d').annotate(s=Sum('amount')).order_by('d')
        )
        per_day = {r['d']: float(r['s'] or 0) for r in rows}
        labels = [(start + BISHKEK_SHIFT + timedelta(days=i)).date()
                  for i in range(days)]
        values = [per_day.get(day, 0.0) for day in labels]

        fig, ax = plt.subplots(figsize=(11, 4))
        ax.bar([d.strftime('%d.%m') for d in labels], values, color='#3b8ed0')
        ax.set_ylabel('Сумма')
        ax.set_title(f'Поступления за {days} дн.')
        ax.grid(axis='y', linestyle='--', alpha=0.3)
        for label in ax.get_xticklabels():
            label.set_rotation(60)
            label.set_fontsize(7)

        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=80, bbox_inches='tight')
        plt.close(fig)  # обязательно закрываем — экономим RAM
        return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

    def report_view(self, request):
        context = dict(
            self.admin_site.each_context(request),
            title='Отчёт по платежам',
            summary=self._summary(),
            chart_week=self._daily_chart(7),
            chart_month=self._daily_chart(30),
            excel_url=reverse('admin:payments_export_excel'),
        )
        return render(request, 'admin/payments/report.html', context)

    # ---------- Excel ----------

    def _build_workbook(self, qs):
        from openpyxl import Workbook

        wb = Workbook()
        ws = wb.active
        ws.title = 'Платежи'
        ws.append([
            'Принято (Бишкек)', 'Сумма', 'Как принято', 'Клиент',
            'Telegram ID', 'Юзернейм', 'ID транзакции',
            'Уверенность OCR, %', 'Дата чека (Бишкек)',
        ])
        for p in qs.order_by('-created_at'):
            ws.append([
                (p.created_at + BISHKEK_SHIFT).strftime('%d.%m.%Y %H:%M'),
                float(p.amount),
                p.get_method_display(),
                (p.client.name if p.client else '') or p.username or p.tg_code,
                p.tg_code,
                p.username,
                p.transaction_id,
                p.ocr_confidence if p.ocr_confidence is not None else '',
                (p.receipt_datetime.strftime('%d.%m.%Y %H:%M')
                 if p.receipt_datetime else ''),
            ])
        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)
        return buf

    def _xlsx_response(self, buf, filename):
        resp = HttpResponse(
            buf.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.'
                         'spreadsheetml.sheet',
        )
        resp['Content-Disposition'] = f'attachment; filename={filename}'
        return resp

    def export_excel(self, request):
        # Даты в фильтре админ вводит по Бишкеку — сравниваем со сдвинутым временем
        qs = Payment.objects.annotate(local_dt=ExpressionWrapper(
            F('created_at') + BISHKEK_SHIFT, output_field=DateTimeField()))
        date_from = request.GET.get('from')
        date_to = request.GET.get('to')
        if date_from:
            qs = qs.filter(local_dt__date__gte=date_from)
        if date_to:
            qs = qs.filter(local_dt__date__lte=date_to)
        return self._xlsx_response(self._build_workbook(qs), 'payments.xlsx')

    @admin.action(description='📥 Экспорт выбранных в Excel')
    def export_selected_excel(self, request, queryset):
        return self._xlsx_response(
            self._build_workbook(queryset), 'payments_selected.xlsx')
