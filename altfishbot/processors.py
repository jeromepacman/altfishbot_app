import array
import random
from datetime import timedelta
from django.db.models import F
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


# commands #########
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
            response = f"{user.role}  @{user.username}"
            bot.sendMessage(update.get_chat().get_id(), response)
            state.name = 'ask_team'


def user_24(bot: TelegramBot, update: Update, state: TelegramState):
    text = update.get_message().get_text()
    if text == '/24h':
        a = TelegramUser.objects.filter(updated_at__gte=now() - timedelta(hours=24)).count(),
        bot.sendMessage(update.get_chat().get_id(), a)
        state.name = 'ask_24h'


# Internal requests ###########

@processor(state_manager, from_states=state_types.Reset, message_types=message_types.Text,
           update_types=update_types.Message)
def post_count(bot: TelegramBot, update: Update, state: TelegramState):
    chat_type = update.get_chat().get_type()
    user_id = update.get_user().get_id()
    text = update.get_message().get_text()

    if chat_type == 'supergroup' and text is not None:
        user = TelegramUser.objects.get(telegram_id=user_id)
        user.post_count += 1
        user.save()
        state.name = 'db_request'


@processor(state_manager, from_states=state_types.Reset, message_types=message_types.Text,
           update_types=update_types.Message)
def user_info(bot: TelegramBot, update: Update, state: TelegramState):
    text = update.get_message().get_text()
    user_id = update.get_user().get_id()
    if text == '/myinfo':
        a = TelegramUser.objects.filter(telegram_id=user_id)
        b = (a.values_list())
        print(len(b))
        for e in a.role:
            print(e)
