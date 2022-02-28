from django.contrib import admin
from django.utils.html import format_html

from . import models


@admin.register(models.TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'telegram_id', 'first_name', 'last_name', 'username', 'has_status', 'role', 'post_count', 'language_code', 'updated_at',
        'joined')
    order_by = ['updated_at']
    filter_by = ['role', 'post_count']
    search_fields = ('telegram_id', 'first_name')
    list_editable = ['has_status']


@admin.register(models.TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'type', 'title', 'username')


admin.site.register(models.TelegramState)
