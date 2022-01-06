from django.contrib import admin

from . import models


@admin.register(models.TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'telegram_id', 'first_name', 'last_name', 'username', 'role', 'language_code', 'updated_at', 'joined')
    order_by = ['- updated_at']


@admin.register(models.TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'type', 'title', 'username')


@admin.register(models.TelegramState)
class TelegramState(admin.ModelAdmin):
    list_display = ('memory', 'name')
