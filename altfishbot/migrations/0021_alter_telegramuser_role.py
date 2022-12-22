# Generated by Django 4.1.4 on 2022-12-22 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('altfishbot', '0020_alter_telegramuser_is_premium_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='role',
            field=models.CharField(blank=True, choices=[('Admin', '🔰 Admin'), ('Whale', '🐳 Whale'), ('Babywhale', '🐋 Babywhale'), ('Dolphin', '🐬 Dolphin'), ('Member', '🐡 Trusted'), ('Hustler', '🚫 Hustler'), ('Bot', '🔷 Bot')], max_length=15, null=True),
        ),
    ]
