# Generated by Django 4.0.6 on 2022-11-25 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('altfishbot', '0018_telegramuser_is_premium'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='warnings',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
