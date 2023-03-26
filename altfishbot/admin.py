from django.contrib import admin, messages
from . import models


@admin.register(models.TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'first_name', 'last_name', 'username', 'has_status', 'role', 'post_count', 'warnings',
                    'is_premium', 'language_code', 'updated_at',
                    'joined']
    ordering = ['-updated_at']
    list_filter = ['role', 'joined']
    search_fields = ['telegram_id', 'first_name', 'username']
    list_editable = ['role']
    actions = ['tag_user', 'untag_user', 'make_member', 'unwarn_user']

    @admin.action(description='Make selected users as trusted')
    def make_member(self, request, queryset):
        updated_count = queryset.update(role='Member', has_status=True)
        self.message_user(request, f'{updated_count} telegram users have been turned to trusted members',
                          messages.SUCCESS)

    @admin.action(description='Tag selected users')
    def tag_user(self, request, queryset):
        updated_count = queryset.update(has_status=True)
        self.message_user(request, f'{updated_count} telegram users were successfully tagged',
                          messages.SUCCESS)

    @admin.action(description='Untagged selected users')
    def untag_user(self, request, queryset):
        updated_count = queryset.update(has_status=True)
        self.message_user(request, f'{updated_count} telegram users were successfully untagged',
                          messages.SUCCESS)

    @admin.action(description='Unwarn selected users')
    def unwarn_user(self, request, queryset):
        updated_count = queryset.update(warnings=0)
        self.message_user(request, f'{updated_count} telegram users were successfully unwarned',
                          messages.SUCCESS)



@admin.register(models.TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'username', 'type', 'title']


@admin.register(models.TelegramState)
class TelegramStateAdmin(admin.ModelAdmin):
    list_display = ['name', 'telegram_user', 'telegram_chat']
