# Generated by Django 3.1.14 on 2022-02-27 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('altfishbot', '0011_auto_20220225_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='language_code',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
