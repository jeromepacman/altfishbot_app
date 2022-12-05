from django.contrib import admin
from .models import BannedWord, Referral


@admin.register(BannedWord)
class BannedWordAdmin(admin.ModelAdmin):
    list_display = ['banned_word']


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['ref_list']