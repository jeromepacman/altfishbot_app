# Generated by Django 4.0.6 on 2022-12-05 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_list', models.CharField(max_length=20)),
            ],
        ),
        migrations.RenameModel(
            old_name='BannedList',
            new_name='BannedWord',
        ),
    ]