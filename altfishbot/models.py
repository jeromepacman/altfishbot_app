from _datetime import date
from django.db import models
from django.db.models import CASCADE
from django_tgbot.models import AbstractTelegramUser, AbstractTelegramChat, AbstractTelegramState
from django_countries.fields import CountryField


class TelegramUser(AbstractTelegramUser):
    language_code = CountryField("lang", max_length=2)
    role = models.CharField(max_length=15, choices=(
        ('Admin', '🔰 Admin'),
        ('Whale', '🐳 Whale'),
        ('Babywhale', '🐋 Babywhale'),
        ('Dolphin', '🐬 Dolphin'),
        ('Member', '❇️ Member'),
        ('Hustler', '🚫 Hustler'),
    ), blank=True, null=True)

    post_count = models.IntegerField(null=True, blank=True)
    joined = models.DateField(default=date.today)
    updated_at = models.DateTimeField(auto_now=True)

    def get_role_display(self):
        return self.get_role_display()




class TelegramChat(AbstractTelegramChat):
    pass


class TelegramState(AbstractTelegramState):
    telegram_user = models.ForeignKey(TelegramUser, related_name='telegram_states', on_delete=CASCADE, blank=True,
                                      null=True)
    telegram_chat = models.ForeignKey(TelegramChat, related_name='telegram_states', on_delete=CASCADE, blank=True,
                                      null=True)

    class Meta:
        unique_together = ('telegram_user', 'telegram_chat')