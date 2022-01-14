import random
from datetime import timedelta
from django.utils.timezone import now
from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.keyboardbutton import KeyboardButton
from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup
from django_tgbot.types.update import Update
from .bot import state_manager
from .models import TelegramState, TelegramUser
from .bot import TelegramBot
from .quotes import QUOTES_STRINGS


# commands #########
@processor(state_manager, from_states=state_types.Reset, message_types=message_types.Text,
           update_types=update_types.Message)
def quotes(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    text = update.get_message().get_text()
    if text == '/quote':
        quote = random.choices(QUOTES_STRINGS)
        bot.sendMessage(chat_id, quote[0])
        state.name = 'ask_quote'


@processor(state_manager, from_states=state_types.Reset, message_types=message_types.Text,
           update_types=update_types.Message)
def role(bot: TelegramBot, update: Update, state: TelegramState):
    text = update.get_message().get_text()
    user_id = update.get_user().get_id()
    if text == '/i':
            a = TelegramUser.objects.get(telegram_id=user_id)
            if a.role is not None:
                t = f' {a} is {a.get_role_display()}'
            else:
                t = f' {a} has no status'
            bot.sendMessage(update.get_chat().get_id(), t)
            state.name = 'role'


@processor(state_manager, from_states=state_types.Reset, message_types=message_types.Text,
           update_types=update_types.Message)
def team_ask(bot: TelegramBot, update: Update, state: TelegramState):
    text = update.get_message().get_text()
    if text == '/ad':
        for user in TelegramUser.objects.filter(role='🔰 Admin'):
            response = f'@{user.username}'
            bot.sendMessage(update.get_chat().get_id(), response)
            state.name = 'team'


@processor(state_manager, from_states=state_types.Reset, message_types=message_types.Text,
           update_types=update_types.Message)
def user_24(bot: TelegramBot, update: Update, state: TelegramState):

    text = update.get_message().get_text()
    if text == '/active':
        n = TelegramUser.objects.filter(updated_at__gte=now() - timedelta(hours=24)).count(),
        f = {n}
        bot.sendMessage( f, f'users')
        state.name = 'actives'


# Internal direct requests #######################
@processor(state_manager, from_states=state_types.Reset, message_types=message_types.SupergroupChatCreated,
           update_types=update_types.Message)
def post_count(bot: TelegramBot, update: Update, state: TelegramState):
    chat_type = update.get_chat().get_type()
    user_id = update.get_user().get_id()
    text = update.get_message().get_text()
    if chat_type == 'supergroup' and len(text) > 15:
        user = TelegramUser.objects.get(telegram_id=user_id)
        user.post_count += 1
        user.save()
        state.name = 'count_post'


#@processor(state_manager, from_states=state_types.Reset, message_types=message_types.LeftChatMember,
##           update_types=update_types.Message)
#def user_flush(bot: TelegramBot, update: Update, state: TelegramState):
#    user_id = update.get_user().get_id()
#    v = TelegramUser.objects.get(telegram_id=user_id)

#    if v.status = 'left':
#        v.delete()




