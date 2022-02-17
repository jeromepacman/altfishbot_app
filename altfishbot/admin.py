from django.contrib import admin

from . import models


@admin.register(models.TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'telegram_id', 'first_name', 'last_name', 'username', 'role', 'post_count', 'language_code', 'updated_at',
        'joined')
    order_by = ['updated_at']
    filter_by = ['role', 'post_count']
    search_fields = ('telegram_id', 'first_name')


@admin.register(models.TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'type', 'title', 'username')


admin.site.register(models.TelegramState)
