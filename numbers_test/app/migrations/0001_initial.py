# Generated by Django 4.0.5 on 2022-06-24 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_name', models.CharField(max_length=100)),
                ('currency_rate_to_rubles', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index_in_table', models.PositiveIntegerField()),
                ('order_id', models.PositiveIntegerField()),
                ('incoming_date', models.DateField()),
                ('total_cost_in_dollars', models.PositiveIntegerField()),
                ('total_cost_in_rubles', models.PositiveIntegerField()),
            ],
        ),
    ]
