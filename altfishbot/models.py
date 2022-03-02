from _datetime import date
from django.db import models
from django.db.models import CASCADE
from django.utils.html import format_html
from django_tgbot.models import AbstractTelegramUser, AbstractTelegramChat, AbstractTelegramState


class TelegramUser(AbstractTelegramUser):
    language_code = models.CharField("Lang", max_length=15, null=True, blank=True)
    role = models.CharField(max_length=15, choices=(
        ('Admin', '🔰 Admin'),
        ('Whale', '🐳 Whale'),
        ('Babywhale', '🐋 Babywhale'),
        ('Dolphin', '🐬 Dolphin'),
        ('Member', '🐡 Member'),
        ('Hustler', '🚫 Hustler'),
        ('Bot', '🔷 Bot'),), blank=True, null=True)

    post_count = models.IntegerField("posts", default=0)
    joined = models.DateField(default=date.today)
    updated_at = models.DateTimeField(auto_now=True)
    has_status = models.BooleanField("Mb", default=False)

    def __str__(self):
        return f' {self.name()}'

    def name(self):
        name = self.first_name
        if self.last_name is not None:
            name += f' {self.last_name}'
        if self.username is not None:
            name = f' @{self.username}'
        return name


class TelegramChat(AbstractTelegramChat):
    pass


class TelegramState(AbstractTelegramState):
    telegram_user = models.ForeignKey(TelegramUser, related_name='telegram_states', on_delete=CASCADE, blank=True,
                                      null=True)
    telegram_chat = models.ForeignKey(TelegramChat, related_name='telegram_states', on_delete=CASCADE, blank=True,
                                      null=True)

    class Meta:
        unique_together = ('telegram_user', 'telegram_chat')

    def __str__(self):
        if self.name is not None:
            return f'{self.name}'
        return f'{self.telegram_user}'
