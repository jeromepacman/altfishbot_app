from django.contrib import admin, messages
from . import models


@admin.register(models.TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'first_name', 'last_name', 'username', 'has_status', 'role', 'post_count', 'warnings',
                    'is_premium', 'language_code', 'updated_at',
                    'joined']
    ordering = ['-updated_at']
    list_filter = ['role', 'joined', 'post_count']
    search_fields = ['telegram_id', 'first_name', 'username']
    list_editable = ['role']
    actions = ['tag_user', 'make_member']

    @admin.action(description='Grant selected as members')
    def make_member(self, request, queryset):
        updated_count = queryset.update(role='Member', has_status=True)
        self.message_user(request, f'{updated_count} telegram users were successfully granted',
                          messages.SUCCESS)

    @admin.action(description='Tag selected users')
    def tag_user(self, request, queryset):
        updated_count = queryset.update(has_status=True)
        self.message_user(request, f'{updated_count} telegram users were successfully tagged',
                          messages.SUCCESS)


@admin.register(models.TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'username', 'type', 'title']


@admin.register(models.TelegramState)
class TelegramStateAdmin(admin.ModelAdmin):
    list_display = ['name', 'telegram_user', 'telegram_chat']