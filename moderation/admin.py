from django.contrib import admin
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