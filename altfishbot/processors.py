import random
from datetime import timedelta

import requests
from django.utils.timezone import now

from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.inlinekeyboardbutton import InlineKeyboardButton
from django_tgbot.types.inlinekeyboardmarkup import InlineKeyboardMarkup
from django_tgbot.types.keyboardbutton import KeyboardButton
from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup
from django_tgbot.types.replykeyboardremove import ReplyKeyboardRemove
from django_tgbot.types.update import Update
from moderation.models import BannedWord, WarningText, Rule, Quote
from .bot import TelegramBot
from .bot import state_manager
from .credentials import OWNER, JIM, CHAT_INVITE_LINK
from .helpers import get_market_cap
from .models import TelegramState, TelegramUser
from .quotes import QUOTES_STRINGS, ACTIVE_ADMINS_LIST, MEMBERS_ROLES, SERV_MSG


# commands #########
# Internal direct requests
# LEFT CHAT MEMBER #######################
@processor(state_manager, from_states=state_types.All, message_types=[message_types.LeftChatMember],
           update_types=update_types.ChatMember)
def outdoor(bot: TelegramBot, update: Update, state: TelegramState):
    msg_id = update.get_message().get_message_id()
    chat_id = update.get_chat().get_id()
    left_id = update.get_message().get_from().get_id()

    if bot.getChatMember(chat_id, left_id).status in ['left', 'banned']:
        try:
            TelegramUser.objects.get(telegram_id=left_id).delete()
        except TelegramUser.DoesNotExist:
            bot.sendMessage(OWNER, text="user does not exist")

    bot.deleteMessage(chat_id, msg_id)


# NEW CHAT MEMBER #######################
@processor(state_manager, from_states=state_types.All, message_types=[message_types.NewChatMembers],
           update_types=update_types.Message)
def indoor(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    msg_id = update.get_message().get_message_id()
    new_id = update.get_user().get_id()

    if bot.getChatMember(chat_id, new_id).status in ['member']:
        try:
            TelegramUser.objects.get(telegram_id=new_id).has_status=True
        except TelegramUser.DoesNotExist:
            bot.sendMessage(OWNER, text="user does not exist")

    bot.deleteMessage(chat_id, msg_id)

# CHECKS & UPDATES#######
#   FORWARDS  ####
@processor(state_manager, from_states=state_types.All,
           exclude_message_types=[message_types.NewChatMembers, message_types.LeftChatMember],
           update_types=update_types.Message)
def post_count(bot: TelegramBot, update: Update, state: TelegramState):
    chat_type = update.get_chat().get_type()
    chat_id = update.get_chat().get_id()
    user_id = update.get_user().get_id()
    msg_id = update.get_message().get_message_id()

    if chat_type == 'supergroup':
        user = TelegramUser.objects.get(telegram_id=user_id)
        forward_from_channel = update.get_message().get_forward_from_chat()
        forward_from = update.get_message().get_forward_from()

        if forward_from_channel and not user.role:
            if WarningText.objects.filter(bannedword__banned_word='!forward_from_channel').exists():
                warn_text = WarningText.objects.get(bannedword__banned_word='!forward_from_channel')
                user.warnings += 1
                if user.warnings > warn_text.warning_number:
                    bot.kickChatMember(chat_id, user_id)
                else:
                    bot.sendMessage(chat_id, f"{user.name()} {warn_text}")
                    user.save()
                bot.deleteMessage(chat_id, msg_id)

        elif forward_from and not user.role:
            if WarningText.objects.filter(bannedword__banned_word='!forward_from').exists():
                warn_text = WarningText.objects.get(bannedword__banned_word='!forward_from')
                user.warnings += 1
                if user.warnings > warn_text.warning_number:
                    bot.kickChatMember(chat_id, user_id)
                else:
                    bot.sendMessage(chat_id, f"{user.name()} {warn_text}")
                    user.save()
                bot.deleteMessage(chat_id, msg_id)

@processor(state_manager, from_states=state_types.Reset, message_types=[message_types.Text],
           update_types=update_types.Message)
def text_count(bot: TelegramBot, update: Update, state: TelegramState):
    chat_type = update.get_chat().get_type()
    chat_id = update.get_chat().get_id()
    text = update.get_message().get_text()
    user_id = update.get_user().get_id()
    msg_id = update.get_message().get_message_id()

    if chat_type == 'supergroup':
        words = BannedWord.objects.values_list('banned_word', flat=True)
        a = TelegramUser.objects.get(telegram_id=user_id)
        for w in words:
            if w in text.lower() and not a.role:
                warn_text = WarningText.objects.get(bannedword__banned_word=w)
                a.warnings += 1
                if a.warnings > warn_text.warning_number:
                    bot.deleteMessage(chat_id, msg_id)
                    bot.kickChatMember(chat_id, user_id)
                    break
                else:
                    bot.deleteMessage(chat_id, msg_id)
                    bot.sendMessage(chat_id, f"{a.name()} {warn_text})")
                    a.save()
                    break

        else:
            a.updated_at = now()
            if len(text) >= 4:
                a.post_count += 1
            a.save()


@processor(state_manager, from_states=state_types.All, message_types=message_types.Text,
           update_types=update_types.Message)
def group_cmd(bot: TelegramBot, update: Update, state: TelegramState):
    chat_type = update.get_chat().get_type()
    chat_id = update.get_chat().get_id()
    text = update.get_message().get_text()
    user_id = update.get_user().get_id()
    user_name = update.get_message().get_from()
    chat_direct = update.get_message().get_from().get_id()
    msg_id = update.get_message().get_message_id()

    if chat_type == 'supergroup' and text.startswith('/'):

        if text == '/quote' and user_id == OWNER or user_id == JIM:
            quote = Quote.objects.filter(active=True).order_by('?')[0]
            bot.sendMessage(chat_id, f'🔈"{quote.text}"\n©️{quote.author}', parse_mode='HTML')

        elif text == '/quotedb' and user_id == OWNER or user_id == JIM:
            quote = Quote.objects.order_by('?')[0]
            bot.sendMessage(chat_id, {quote}, parse_mode='HTML')

        elif text == '/strike':
            bot.sendDice(chat_id, '🎳')

        elif text == '/reg':
            rules = Rule.objects.get(pk=1)
            bot.sendMessage(user_id, f'{rules}', parse_mode='html')

        elif text == '/role' or text == '/role@AltFishBot':
            sender = update.get_message().get_reply_to_message().get_from().get_id()
            if sender is not None:
                try:
                    c = TelegramUser.objects.get(telegram_id=sender)
                except TelegramUser.DoesNotExist:
                    bot.sendMessage(chat_id, 'no data')
                else:
                    if c.role is not None:
                        response = f'Hey {user_name.first_name}\n{c} is {c.get_role_display()}'
                        bot.sendMessage(chat_id, response)
                    else:
                        bot.sendMessage(chat_id, 'no status found')

        elif text == '/rolep':
            sender = update.get_message().get_reply_to_message().get_from().get_id()
            if sender is not None:
                c = TelegramUser.objects.get(telegram_id=sender)
                if c.role is not None:
                    response = f'Hey {user_name.first_name}\n{c} is {c.get_role_display()}'
                    bot.sendMessage(user_id, response)
                else:
                    bot.sendMessage(user_id, 'no status found')

        elif text == '/status' or text == '/status@AltFishBot':
            b = TelegramUser.objects.get(telegram_id=user_id)
            if b.role is not None:
                c = f'{b.get_role_display()}'
                bot.sendMessage(chat_id, f'Hi {b.first_name} 😎\nYour Status: \n{c}')
            else:
                bot.sendMessage(chat_id, f"😶 You don't have any status {b.first_name}")

        elif text == '/promote' and user_id == OWNER:
            sender = update.get_message().get_reply_to_message().get_from().get_id()
            if sender is not None:
                d = TelegramUser.objects.get(telegram_id=sender)
                if d.role is not None:
                    if d.role == "Member":
                        response = f'▫️You got a new status in AltWhales 🐳:\n  ➖ {d.get_role_display()}  ➖  '
                        bot.sendMessage(sender, response)
                    else:
                        response = f'📦️{d} got a new status:\n    ➖ {d.get_role_display()}  ➖  '
                        bot.sendMessage(chat_id, response)
                else:
                    bot.sendMessage(OWNER, f'user {d} has no role')

        elif text == '/clear' and user_id == OWNER or user_id == JIM:
            sender = update.get_message().get_reply_to_message().get_from().get_id()
            if sender is not None:
                h = TelegramUser.objects.get(telegram_id=sender)
                h.warnings = 0
                h.save()
                bot.sendMessage(sender, f"✅ warnings cleared")

        elif text == '/db' and user_id == OWNER:
            try:
                tourist = TelegramUser.objects.filter(has_status=False)
                tourist.delete()
            except:
                bot.sendMessage(chat_id=OWNER, text="Data failed")
            else:
                bot.sendMessage(chat_id=OWNER, text=f"{tourist.count()} tourists deleted")

        elif text == '/purge' and user_id == OWNER:
            try:
                inactive = TelegramUser.objects.filter(updated_at__lt=now() - timedelta(days=180)).exclude(
                    role__isnull=False)
                inactive.delete()
            except:
                bot.sendMessage(chat_id=OWNER, text='Error db action')
            else:
                bot.sendMessage(chat_id=OWNER, text=f'{inactive.count()} users purged')

        elif text == "/cap" and user_id == OWNER or user_id == JIM:
            bot.sendMessage(chat_id, get_market_cap(), parse_mode='html')


        elif text == '/flag' and user_id == OWNER or user_id == JIM:
            sender = update.get_message().get_reply_to_message().get_from().get_id()
            sender_msg = update.get_message().get_reply_to_message().get_message_id()
            if sender is not None:
                f = TelegramUser.objects.get(telegram_id=sender)
                f.warnings += 1
                f.save()
                bot.deleteMessage(chat_id, sender_msg)

        elif text.startswith('/f @') and user_id == OWNER or user_id == JIM:
            flag = text[4:]
            try:
                b = TelegramUser.objects.get(username=flag)
            except TelegramUser.DoesNotExist:
                bot.sendMessage(OWNER, 'unknown user')
            else:
                b = b.telegram_id
                sta = bot.getChatMember(chat_id, b).status
                bot.sendMessage(OWNER, sta)

        elif text.startswith('/f ') and text[3:].isdigit() and user_id == OWNER or user_id == JIM:
            flag = text[3:]
            try:
                b = TelegramUser.objects.get(telegram_id=flag)
            except TelegramUser.DoesNotExist:
                bot.sendMessage(OWNER, 'unknown user')
            else:
                b = b.telegram_id
                sta = bot.getChatMember(chat_id, b).status
                bot.sendMessage(OWNER, sta)

        elif text.startswith('/k @') and user_id == OWNER or user_id == JIM:
            klag = text[4:]
            try:
                b = TelegramUser.objects.get(username=klag)
            except TelegramUser.DoesNotExist:
                bot.sendMessage(OWNER, 'unknown user')
            else:
                b = b.telegram_id
                bot.kickChatMember(chat_id, b)
                sta = bot.getChatMember(chat_id, b).status
                bot.sendMessage(OWNER, sta)

        elif text.startswith('/k ') and text[3:].isdigit() and user_id == OWNER or user_id == JIM:
            klag = text[3:]
            try:
                b = TelegramUser.objects.get(telegram_id=klag)
            except TelegramUser.DoesNotExist:
                bot.sendMessage(OWNER, 'unknown user')
            else:
                b = b.telegram_id
                bot.kickChatMember(chat_id, b)
                sta = bot.getChatMember(chat_id, b).status
                bot.sendMessage(OWNER, sta)


        elif text == '/up' or text == '/up@AltFishBot':
            a = TelegramUser.objects.get(telegram_id=user_id)
            if a.role == "Hustler":
                bot.sendMessage(chat_id, SERV_MSG[0])
            else:
                bot.sendMessage(
                    chat_direct,
                    f'🐳',
                    reply_markup=ReplyKeyboardMarkup.a(resize_keyboard=True, keyboard=[
                        [KeyboardButton.a('Rules of the group'), KeyboardButton.a('Invite link')],
                        [KeyboardButton.a('Admins list'), KeyboardButton.a('Hustlers list')],
                        [KeyboardButton.a('Group status'), KeyboardButton.a('My status')],
                        [KeyboardButton.a('Market news'), KeyboardButton.a('Gecko trendy coins')],
                        [KeyboardButton.a('Market trend'), KeyboardButton.a('Channel')],
                    ])
                )

        bot.deleteMessage(chat_id, msg_id)


# ADMIN #######################
# Private chat actions  #######################

# @processor(state_manager, from_states=state_types.Reset, success='asked_quote', message_types=[message_types.Text], update_types=update_types.Message)
# def ask_quote(bot: TelegramBot, update: Update, state: TelegramState):
#     chat_type = update.get_chat().get_type()
#     chat_id = update.get_chat().get_id()
#     text = update.get_message().get_text()
#     if chat_type == 'private' and chat_id == '342785208' and text == 'add quote':
#         bot.sendMessage(chat_id, "⚪️ Ok\nsend me a quote..")
#
#
#
# @processor(state_manager, from_states='asked_quote', success='ask_author', message_types=message_types.Text, update_types=update_types.Message)
# def get_author(bot: TelegramBot, update: Update, state: TelegramState):
#     chat_id = update.get_chat().get_id()
#     quote_text = update.get_message().get_text()
#     state.set_memory({'q_text': quote_text})
#     bot.sendMessage(chat_id, "send author name..")
#
#
# @processor(state_manager, from_states='ask_author', smessage_types=message_types.Text, update_types=update_types.Message)
# def get_final(bot: TelegramBot, update: Update, state: TelegramState):
#     chat_id = update.get_chat().get_id()
#     author = update.get_message().get_text()
#     grab_quote = state.get_memory()['q_text']
#     total = f"🔈{grab_quote}\n©{author}"
#     a = TelegramUser.objects.get(telegram_id=chat_id)
#     bot.sendMessage(chat_id, 'in the box')
#     state.reset_memory()
#     state.set_name('')


#    #### BOT IN PRIVATE CHAT ######
@processor(state_manager, from_states=state_types.All, message_types=[message_types.Text],
           update_types=update_types.Message)
def resp_kb(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    text = update.get_message().get_text()
    msg_id = update.get_message().get_message_id()
    chat_type = update.get_chat().get_type()

    if chat_type == 'private':
        try:
            user = TelegramUser.objects.get(telegram_id=chat_id)
        except TelegramUser.DoesNotExist:
            bot.sendMessage(chat_id, SERV_MSG[0], reply_markup=ReplyKeyboardRemove.a(remove_keyboard=True))
            bot.leaveChat(chat_id)
        else:
            if text == 'My status':
                if user.role:
                    st = f'{user.get_role_display()}\n'
                    bot.sendMessage(chat_id,
                                    f"<b>{user.first_name}</b> 😎\n\nId {user.telegram_id}\n\n\nYour Status is {st}\nYou're in the group since {user.joined}\n\n<i>Date might be incorrect, i'm still in beta</i> 😬",
                                    parse_mode="html")
                else:
                    bot.sendMessage(chat_id, "\nYou don't have any status yet 😶")

            elif text == 'Admins list':
                bot.sendMessage(chat_id, ACTIVE_ADMINS_LIST, parse_mode='html')

            elif text == 'Group status':
                active_members = TelegramUser.objects.filter(updated_at__gte=now() - timedelta(hours=24)).count()
                bot.sendMessage(chat_id,
                                f'<u>Members roles</u> \n\n{MEMBERS_ROLES} \n🌐 <b>{active_members} users are currently active</b>',
                                parse_mode="html")

            elif text == 'Hustlers list':
                if user.role and user.role not in ['Hustler']:
                    bot.sendMessage(chat_id, '\nMostly scams..\n')
                    for user in TelegramUser.objects.filter(role="Hustler"):
                        bot.sendMessage(chat_id, f'{user.name()} id_{user.telegram_id} {user.get_role_display()}')
                else:
                    bot.sendMessage(chat_id, SERV_MSG[1])

            elif text == 'Market news':
                if user.role in ['Admin', 'Whale', 'Babywhale', 'Dolphin']:
                    news = requests.get(url='https://min-api.cryptocompare.com/data/v2/news/?lang=EN')
                    api = news.json()
                    data = api["Data"][:5]
                    for x in data:
                        title = x["title"]
                        url = x["url"]
                        source = x["source"]
                        response = f'🌎{source.title()}\n<a href="{url}">{title}</a>'
                        bot.sendMessage(chat_id, {response}, disable_web_page_preview=True, parse_mode='html')
                else:
                    bot.sendMessage(chat_id, SERV_MSG[1])

            elif text == 'Gecko trendy coins':
                if user.role in ['Admin', 'Whale', 'Babywhale', 'Dolphin']:
                    request = requests.get(url='https://api.coingecko.com/api/v3/search/trending')
                    result = request.json()
                    coins = result["coins"]
                    url = f'https://coingecko.com/coins/'
                    bot.sendMessage(chat_id, text='📈 Trending coins searched on Gecko:', parse_mode='html')
                    for x in coins:
                        symbol = x["item"]["symbol"]
                        num = x["item"]["slug"]
                        response = f'➖ <a href="{url}{num}">{symbol}</a>'
                        bot.sendMessage(chat_id, response, disable_web_page_preview=True, parse_mode='html')
                else:
                    bot.sendMessage(chat_id, SERV_MSG[1])

            elif text == 'Rules of the group':
                user.has_status = True
                Rule.objects.all()
                rules = Rule.objects.filter(active=True)[0]
                if rules is not None:
                    bot.sendMessage(chat_id, f'appreciated that 😉\n\n {rules}', parse_mode='html')


            elif text == 'Channel':
                bot.sendMessage(chat_id,
                                "Go to @altcoinwhales\n\nCharts from channel admins 🐳:\n➖Artem\n➖Excavo\n➖RocketBomb\n➖LA440\n➖Liquidity Hunter\n➖Edward Morra\n➖Crypto Cove\n& more...\n",
                                reply_markup=InlineKeyboardMarkup.a(
                                    inline_keyboard=[[InlineKeyboardButton.a('Go', url='t.me/altcoinwhales')]]))

            elif text == 'Invite link':
                if user.role and user.role not in ['Hustler']:
                    bot.sendMessage(chat_id, f'—————Your invite link—————\n{CHAT_INVITE_LINK}\n', parse_mode="html",
                                    disable_web_page_preview=True)
                else:
                    bot.sendMessage(chat_id, SERV_MSG[1])

            elif text == "Market trend":
                if user.role in ['Admin', 'Whale', 'Babywhale', ' Dolphin']:
                    bot.sendMessage(chat_id, get_market_cap(), parse_mode='html')
                else:
                    bot.sendMessage(chat_id, SERV_MSG[1])


            elif text == '/start' or text == '/up' or text == '/up@AltBabybot' or text == '/up@AltFishBot':
                bot.sendMessage(
                    chat_id,
                    f'🐳',
                    reply_markup=ReplyKeyboardMarkup.a(resize_keyboard=True, keyboard=[
                        [KeyboardButton.a('Rules of the group'), KeyboardButton.a('Invite link')],
                        [KeyboardButton.a('Admins list'), KeyboardButton.a('Hustlers list')],
                        [KeyboardButton.a('Group status'), KeyboardButton.a('My status')],
                        [KeyboardButton.a('Market news'), KeyboardButton.a('Gecko trendy coins')],
                        [KeyboardButton.a('Market trend'), KeyboardButton.a('Channel')],
                    ])
                )

            elif text =='/reg':
                pass

            else:
                bot.sendMessage(chat_id, SERV_MSG[3])

            bot.deleteMessage(chat_id, msg_id)
            user.updated_at = now()
            user.save()