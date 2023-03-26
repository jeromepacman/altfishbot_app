from django.contrib import admin, messages
from . import models


class OrderItemInline(admin.TabularInline):
    model = models.BannedWord
    extra = 0


@admin.register(models.WarningText)
class WarningTextAdmin(admin.ModelAdmin):
    list_display = ['warning_text', 'warning_number']
    inlines = [OrderItemInline]


@admin.register(models.BannedWord)
class BannedWordAdmin(admin.ModelAdmin):
    list_display = ['banned_word', 'warning_text']
    list_editable = ['warning_text']


@admin.register(models.Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ['rules_text', 'active']
    list_editable = ['rules_text', 'active']
    list_display_links = None


@admin.register(models.WelcomeMessage)
class WelcomeMessageAdmin(admin.ModelAdmin):
    list_display = ['welcome_text', 'active']
    list_editable = ['welcome_text', 'active']
    list_display_links = None


@admin.register(models.Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['text', 'author', 'active']
    actions = ['actives', 'inactives']

    @admin.action(description='Make active')
    def actives(self, request, queryset):
        updated_count = queryset.update(active=True)
        self.message_user(request, f'{updated_count} quotes enabled', messages.SUCCESS)

    @admin.action(description='Make inactive')
    def inactives(self, request, queryset):
        updated_count = queryset.update(active=False)
        self.message_user(request, f'{updated_count} quotes disabled', messages.SUCCESS)





