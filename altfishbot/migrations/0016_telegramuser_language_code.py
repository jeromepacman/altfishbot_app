# Generated by Django 3.1.14 on 2022-03-10 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('altfishbot', '0015_remove_telegramuser_language_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='language_code',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
