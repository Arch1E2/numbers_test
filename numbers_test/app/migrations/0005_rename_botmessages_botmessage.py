# Generated by Django 4.0.5 on 2022-06-25 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_rename_message_is_send_date_botmessages_message_send_date'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BotMessages',
            new_name='BotMessage',
        ),
    ]
