# Generated by Django 4.0.5 on 2022-06-25 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_cost_in_rubles_after_comma',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
