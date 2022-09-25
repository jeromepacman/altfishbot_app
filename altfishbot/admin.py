from django.contrib import admin

from . import models


@admin.register(models.TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'telegram_id', 'first_name', 'last_name', 'username', 'has_status', 'role', 'is_premium', 'post_count', 'language_code', 'updated_at',
        'joined')
    ordering = ('-updated_at',)
    filter_by = ['role', 'post_count']
    search_fields = ('telegram_id', 'first_name')
    list_editable = ['has_status', 'role']


@admin.register(models.TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'type', 'title', 'username')


@admin.register(models.TelegramState)
class TelegramStateAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram_user', 'telegram_chat')