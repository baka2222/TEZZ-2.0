import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0020_clientad_currency_alter_clientad_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_code', models.CharField(blank=True, default='', max_length=50, verbose_name='Telegram ID')),
                ('username', models.CharField(blank=True, default='', max_length=150, verbose_name='Юзернейм')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма')),
                ('method', models.CharField(choices=[('ocr', 'OCR (авто)'), ('admin', 'Админ (вручную)')], max_length=10, verbose_name='Как принято')),
                ('transaction_id', models.CharField(blank=True, db_index=True, default='', help_text='Используется для защиты от повторной отправки одного чека.', max_length=100, verbose_name='ID транзакции (из чека)')),
                ('ocr_confidence', models.FloatField(blank=True, null=True, verbose_name='Уверенность OCR, %')),
                ('receipt_datetime', models.DateTimeField(blank=True, null=True, verbose_name='Дата/время на чеке')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Принято')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='client.client', verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Платёж',
                'verbose_name_plural': 'Платежи',
                'ordering': ['-created_at'],
            },
        ),
    ]
