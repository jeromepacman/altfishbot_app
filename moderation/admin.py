from django.contrib import admin
from . import models


class OrderItemInline(admin.TabularInline):
    model = models.BannedWord
    extra = 1


@admin.register(models.WarningText)
class WarningTextAdmin(admin.ModelAdmin):
    list_display = ['warning_text']
    inlines = [OrderItemInline]


@admin.register(models.BannedWord)
class BannedWordAdmin(admin.ModelAdmin):
    list_display = ['banned_word', 'warning_text']
    list_editable = ['warning_text']