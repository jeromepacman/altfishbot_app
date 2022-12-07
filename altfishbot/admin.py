from django.contrib import admin
from . import models


@admin.register(models.TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'first_name', 'last_name', 'username', 'has_status', 'role', 'posts', 'warned',
                    'is_premium', 'language_code', 'updated_at',
                    'created_at']
    ordering = ['-updated_at']
    list_filter = ['role', 'created_at', 'posts']
    search_fields = ['telegram_id', 'first_name', 'username']
    list_editable = ['role']
    actions = ['tag_user', 'make_member']

    @admin.action(description='Grant selected as members')
    def make_member(self, request, queryset):
        queryset.update(role='Member')

    @admin.action(description='Tag selected users')
    def tag_user(self, request, queryset):
        queryset.update(has_status=True)


@admin.register(models.TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'username', 'type', 'title']


@admin.register(models.TelegramState)
class TelegramStateAdmin(admin.ModelAdmin):
    list_display = ['name', 'telegram_user', 'telegram_chat']