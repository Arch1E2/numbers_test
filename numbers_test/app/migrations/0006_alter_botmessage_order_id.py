# Generated by Django 4.0.5 on 2022-06-25 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_rename_botmessages_botmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botmessage',
            name='order_id',
            field=models.PositiveIntegerField(),
        ),
    ]
