import random
from datetime import timedelta

from django.utils.timezone import now
from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.inlinekeyboardbutton import InlineKeyboardButton
from django_tgbot.types.inlinekeyboardmarkup import InlineKeyboardMarkup
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
        state.name = 'ASKED QUOTE'


@processor(state_manager, from_states=state_types.Reset, message_types=message_types.Text,
           update_types=update_types.Message)
def role(bot: TelegramBot, update: Update, state: TelegramState):
    text = update.get_message().get_text()
    user_id = update.get_user().get_id()
    sender = update.get_message().get_reply_to_message()
    if text == '/i':
        if sender is not None:
            hok = sender.get_from().get_id()
            a = TelegramUser.objects.get(telegram_id=hok)
        else:
            a = TelegramUser.objects.get(telegram_id=user_id)

        if a.role is not None:
            t = f' {a} is {a.get_role_display()}'
        elif a.role is None:
            t = f' {a} has no status'
        else:
            t = f'Bad request, this user is not in the group'

        bot.sendMessage(update.get_chat().get_id(), f"😎 <i>A user asked for a member's status</i>\n {t}", parse_mode='html')
        state.name = 'asked role'


@processor(state_manager, from_states=state_types.Reset, message_types=message_types.Text,
           update_types=update_types.Message)
def team_ask(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    text = update.get_message().get_text()
    if text == '/alist':
        for a in TelegramUser.objects.filter(role='Admin'):
            response = f' @{a.username}'
            bot.sendMessage(chat_id, response)
    state.name = ''


@processor(state_manager, from_states=state_types.All, message_types=message_types.Text,
           update_types=update_types.Message)
def user_24(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    text = update.get_message().get_text()
    if text == '/active':
        n = TelegramUser.objects.filter(updated_at__gte=now() - timedelta(hours=24)).count()
        bot.sendMessage(chat_id, f'{n} users are active')
        state.name = 'active'


# Internal direct requests #######################
@processor(state_manager, from_states=state_types.Reset, message_types=message_types.Text,
           update_types=update_types.Message)
def post_count(bot: TelegramBot, update: Update, state: TelegramState):
    chat_type = update.get_chat().get_type()
    user_id = update.get_user().get_id()
    text = update.get_message().get_text()
    if chat_type == 'supergroup' and len(text) > 15:
        user = TelegramUser.objects.get(telegram_id=user_id)
        user.post_count += 1
        user.save()
        state.name = 'post_count'


@processor(state_manager, from_states=state_types.All, message_types=message_types.LeftChatMember,
           update_types=update_types.Message)
def user_flush(bot: TelegramBot, update: Update, state: TelegramState):
    user_id = update.get_user().get_id()
    user = TelegramUser.objects.get(telegram_id=user_id)
    user.delete()
    admin = TelegramUser.objects.get(telegram_id=34278520)
    bot.sendMessage(admin, f' user {user.first_name} has left')
    state.name = ''


#

# @processor(state_manager, from_states=state_types.Reset, message_types=[message_types.Text])
# def send_keyboards(bot: TelegramBot, update: Update, state: TelegramState):
#     chat_id = update.get_chat().get_id()
#     text = str(update.get_message().get_text())
#
#     if text.lower() in ['normal keyboard', 'regular keyboard']:
#         send_normal_keyboard(bot, chat_id)
#     elif text.lower() in ['inline keyboard']:
#         send_inline_keyboard(bot, chat_id)
#     else:
#         send_options(bot, chat_id)
#
#
# @processor(state_manager, from_states=state_types.All, update_types=[update_types.CallbackQuery])
# def handle_callback_query(bot: TelegramBot, update, state):
#     callback_data = update.get_callback_query().get_data()
#     bot.answerCallbackQuery(update.get_callback_query().get_id(), text='Callback data received: {}'.format(callback_data))
#
#
# def send_normal_keyboard(bot, chat_id):
#     bot.sendMessage(
#         chat_id,
#         text='Here is a keyboard for you!',
#         reply_markup=ReplyKeyboardMarkup.a(
#             one_time_keyboard=True,
#             resize_keyboard=True,
#             keyboard=[
#                 [KeyboardButton.a('Text 1'), KeyboardButton.a('Text 2')],
#                 [KeyboardButton.a('Text 3'), KeyboardButton.a('Text 4')],
#                 [KeyboardButton.a('Text 5')]
#             ]
#         )
#     )
#
#
# def send_inline_keyboard(bot, chat_id):
#     bot.sendMessage(
#         chat_id,
#         text='Here is an inline keyboard for you!',
#         reply_markup=InlineKeyboardMarkup.a(
#             inline_keyboard=[
#                 [
#                     InlineKeyboardButton.a('URL Button', url='https://altcoinwhales.com'),
#                     InlineKeyboardButton.a('Callback Button', callback_data='some_callback_data')
#                 ]
#             ]
#         )
#     )
#
#
# def send_options(bot, chat_id):
#     bot.sendMessage(
#         chat_id,
#         text='I can send you two different types of keyboards!\nSend me `normal keyboard` or `inline keyboard` and I\'ll make one for you ;)',
#         parse_mode=bot.PARSE_MODE_MARKDOWN
#     )