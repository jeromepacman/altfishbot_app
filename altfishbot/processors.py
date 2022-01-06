import array
import random
from datetime import timedelta
from django.utils.timezone import now
from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.types.user import User
from django.db import models
from .bot import state_manager
from .models import TelegramState, TelegramUser
from .bot import TelegramBot
from .quotes import QUOTES_STRINGS


@processor(state_manager, from_states=state_types.All, message_types=message_types.Text,
           update_types=update_types.Message)
def quotes(bot: TelegramBot, update: Update, state: TelegramState):
    text = update.get_message().get_text()
    if text == '/quote':
        quote = random.choices(QUOTES_STRINGS)
        bot.sendMessage(update.get_chat().get_id(), quote[0])
        state.name = 'ask_quote'


@processor(state_manager, from_states=state_types.All, message_types=message_types.Text,
           update_types=update_types.Message)
def team_info(bot: TelegramBot, update: Update, state: TelegramState):
    text = update.get_message().get_text()
    if text == '/team':
        for user in TelegramUser.objects.exclude(role=None):
            response = f'{user.role} @{user.username}'
            bot.sendMessage(update.get_chat().get_id(), response, parse_mode='html')
            state.name = 'ask_team'
            print(response)


@processor(state_manager, from_states=state_types.All, message_types=message_types.Text,
           update_types=update_types.Message)
def user_24(bot: TelegramBot, update: Update, state: TelegramState):
    text = update.get_message().get_text()
    if text == '/24h':
        a = TelegramUser.objects.filter(updated_at__gte=now() - timedelta(hours=24)).count(),
        bot.sendMessage(update.get_chat().get_id(), f'{a} actives')
        state.name = 'ask_24h'








