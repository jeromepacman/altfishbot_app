# Generated by Django 4.1.4 on 2023-01-29 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0006_rule_active_welcomemessage_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('author', models.CharField(default='', max_length=50)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
