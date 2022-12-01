from django.contrib import admin
from .models import BannedList


@admin.register(BannedList)
class BannedListAdmin(admin.ModelAdmin):
    list_display = ['banned_word']