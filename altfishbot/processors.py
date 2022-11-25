import requests
import random
from datetime import timedelta
from django.utils.timezone import now
from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.inlinekeyboardbutton import InlineKeyboardButton
from django_tgbot.types.inlinekeyboardmarkup import InlineKeyboardMarkup
from django_tgbot.types.keyboardbutton import KeyboardButton
from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup
from django_tgbot.types.replykeyboardremove import ReplyKeyboardRemove
from django_tgbot.types.update import Update
from moderation.models import BannedList
from .bot import state_manager
from .models import TelegramState, TelegramUser
from .bot import TelegramBot
from .quotes import QUOTES_STRINGS, ACTIVE_ADMINS_LIST, ADMINS_ID, MEMBERS_ROLES, SERV_MSG
from .helpers import get_tendency, slowdown


# commands #########
# Internal direct requests
# LEFT CHAT MEMBER #######################
@processor(state_manager, from_states=state_types.All, message_types=[message_types.LeftChatMember],
           update_types=update_types.Message)
def door(bot: TelegramBot, update: Update, state: TelegramState):
    msg_id = update.get_message().get_message_id()
    chat_id = update.get_chat().get_id()
    user_id = update.get_user().get_id()
    a = TelegramUser.objects.get(telegram_id=user_id)
    try:
        a.delete()
    except TelegramUser.DoesNotExist:
        bot.sendMessage('342785208', f" User {user_id} is not in the group")
    else:
        bot.deleteMessage(chat_id, msg_id)


# NEW CHAT MEMBER #######################
@processor(state_manager, from_states=state_types.All, message_types=[message_types.NewChatMembers],
           update_types=update_types.Message)
def check(bot: TelegramBot, update: Update, state: TelegramState):
    msg_id = update.get_message().get_message_id()
    chat_id = update.get_chat().get_id()
    user_id = update.get_user().get_id()
    bot.deleteMessage(chat_id, msg_id)
    if bot.getChatMember(chat_id, user_id).status in ['kicked']:
        try:
            TelegramUser.objects.get(telegram_id=user_id).delete()
        except TelegramUser.DoesNotExist:
            bot.sendMessage('342785208', text="user does not exist")

    elif bot.getChatMember(chat_id, user_id).status in ['member']:
        a = TelegramUser.objects.get(telegram_id=user_id)
        a.has_status = True
        a.save()


# CHECKS & UPDATES#######
@processor(state_manager, from_states=state_types.Reset, message_types=[message_types.Text],
           update_types=update_types.Message)
def post_count(bot: TelegramBot, update: Update, state: TelegramState):
    chat_type = update.get_chat().get_type()
    chat_id = update.get_chat().get_id()
    text = update.get_message().get_text()
    user_id = update.get_user().get_id()
    sender = update.get_message().get_reply_to_message()
    user_name = update.get_message().get_from()
    chat_direct = update.get_message().get_from().get_id()
    msg_id = update.get_message().get_message_id()

    if chat_type == 'supergroup':
        words = BannedList.objects.values_list('banned_word', flat=True)
        a = TelegramUser.objects.get(telegram_id=user_id)
        for w in words:
            if w in text.lower():
                bot.deleteMessage(chat_id, msg_id)
                a.warnings += 1
                if a.warnings == 2:
                    bot.kickChatMember(chat_id, user_id)
                    return
                else:
                    bot.sendMessage(chat_id, f"{a.name()} you're not allowed to post that shit, you're warned")
                    a.save()
                    return
        if len(text) >= 4 and not text.startswith('/') and a.warnings < 2:
            a.post_count += 1
            a.updated_at = now()
            a.save()

        if text.startswith('/'):
            if text == '/quote':
                quote = random.choices(QUOTES_STRINGS)
                bot.deleteMessage(chat_id, user_id)
                bot.sendMessage(chat_id, {quote[0]}, parse_mode="html")

            elif text == '/who':
                if sender is not None:
                    hook = sender.get_from().get_id()
                    a = TelegramUser.objects.get(telegram_id=hook)
                    if a.role is not None:
                        response = f'Hey {user_name.first_name}\n{a} is {a.get_role_display()}'
                        bot.sendMessage(chat_id, response)
                    else:
                        bot.sendMessage(chat_id, 'no status found')

            elif text == '/whop':
                if sender is not None:
                    hook = sender.get_from().get_id()
                    a = TelegramUser.objects.get(telegram_id=hook)
                    if a.role is not None:
                        response = f'Hey {user_name.first_name}\n{a} is {a.get_role_display()}'
                        bot.sendMessage(user_id, response)
                    else:
                        bot.sendMessage(user_id, 'no status found')

            elif text == '/inf':
                b = TelegramUser.objects.get(telegram_id=user_id)
                if b.role is not None:
                    c = f'{b.get_role_display()}'
                    bot.sendMessage(chat_id, f'Hi {b.first_name} 😎\nYour Status: \n{c}')
                else:
                    bot.sendMessage(chat_id, f"😶 You don't have any status {b.first_name}")

            elif text == '/promote' and user_id == '342785208':
                if sender is not None:
                    hook = sender.get_from().get_id()
                    a = TelegramUser.objects.get(telegram_id=hook)
                    if a.role is not None:
                        if a.role == "Member":
                            response = f'▫️You got a new status in Alt Whales 🐳:\n  ➖ {a.get_role_display()}  ➖  '
                            bot.sendMessage(hook, response)
                        else:
                            response = f'▫️{a} got a new status:\n    ➖ {a.get_role_display()}  ➖  '
                            bot.sendMessage(chat_id, response)
                    else:
                        bot.sendMessage(user_id, f'user {a} has no role')
                else:
                    bot.sendMessage(chat_id, 'Bad request')

            elif text == '/db' and user_id == '342785208':
                try:
                    TelegramUser.objects.filter(has_status=False).delete()
                except:
                    bot.sendMessage(chat_id='342785208', text="Data failed")
                else:
                    bot.sendMessage(chat_id='342785208', text="Data purged")

            elif text == "/cap" and user_id == '342785208':
                cap = requests.get(url='https://api.coingecko.com/api/v3/global')
                fear = requests.get(url='https://api.alternative.me/fng/?limit=1')
                tendency = requests.get(
                    url='https://api.cryptometer.io/trend-indicator-v3/?api_key=KLT7vnP42Bf4k55z07sA9ImHpVd2lN11s4B3854Y')
                result_1 = cap.json()
                result_2 = fear.json()
                result_3 = tendency.json()
                data = result_1["data"]
                change = data["market_cap_change_percentage_24h_usd"]
                btc = data["market_cap_percentage"]["btc"]
                eth = data["market_cap_percentage"]["eth"]
                change = round(change, 2)
                change_price = '{:,}'.format(change)
                btc = round(btc, 2)
                domi_btc = '{:,}'.format(btc)
                eth = round(eth, 2)
                domi_eth = '{:,}'.format(eth)
                data2 = result_2["data"][0]
                feeling = data2["value_classification"]
                number = data2["value"]
                data3 = result_3["data"][0]
                buy = data3["buy_pressure"]
                sell = data3["sell_pressure"]
                score = data3["trend_score"]
                buy = round(buy)
                sell = round(sell)
                score = round(score)
                score = get_tendency(score)
                total = f' 📊 <b>Total market change:</> {change_price}% <i>(last 24 hours)</>\n🪙 <b>Bitcoin dominance:</> {domi_btc}%\n🌑 <b>Ethereum dominance:</> {domi_eth}%\n' \
                        f'😵 <b>Fear&Greed index: </>{feeling} ({number}|100)\n\n' \
                        f' 〽️<b>Current market trend:</> {score} <i>(last 4 hours)</>\n🐮 <b>Buy pressure:</> {buy}%\n🐻 <b>Sell pressure:</> {sell}%'
                bot.sendMessage(chat_id, total, parse_mode='html')

            elif text == '/up' or text == '/up@AltBabybot' or text == '/up@AltFishBot':
                a = TelegramUser.objects.get(telegram_id=user_id)
                if a.role == "Hustler":
                    bot.sendMessage(chat_id, SERV_MSG[0])
                else:
                    bot.sendMessage(
                        chat_direct,
                        f'🐳\n',
                        reply_markup=ReplyKeyboardMarkup.a(resize_keyboard=True, keyboard=[
                            [KeyboardButton.a('Rules of the group'), KeyboardButton.a('Active users')],
                            [KeyboardButton.a('Admins list'), KeyboardButton.a('Hustlers list')],
                            [KeyboardButton.a('Group status'), KeyboardButton.a('My status')],
                            [KeyboardButton.a('Market news'), KeyboardButton.a('Gecko trendy coins')],
                            [KeyboardButton.a('Market trend'), KeyboardButton.a('Quote')],
                        ])
                    )


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
        bot.deleteMessage(chat_id, msg_id)
        try:
            user = TelegramUser.objects.get(telegram_id=chat_id)
        except TelegramUser.DoesNotExist:
            bot.sendMessage(chat_id, SERV_MSG[0], reply_markup=ReplyKeyboardRemove.a(remove_keyboard=True))
            bot.leaveChat(chat_id)
        else:
            user.updated_at = now()
            user.save()
            if user.role == "Hustler" or not user.has_status:
                bot.sendMessage(chat_id, SERV_MSG[0])
                bot.leaveChat(chat_id)
            else:
                if text == 'My status':
                    if user.role:
                        st = f'{user.get_role_display()}\n'
                        bot.sendMessage(chat_id,
                                        f"<b>{user.first_name}</b> 😎\n\n\nYour Status is {st}\nYou're in the group since {user.joined}\n\n<i>Date might be incorrect, i'm still in beta</i> 😬",
                                        parse_mode="html")
                    else:
                        bot.sendMessage(chat_id, "\nYou don't have any status yet 😶")

                elif text == 'Admins list':
                    bot.sendMessage(chat_id, ACTIVE_ADMINS_LIST, parse_mode='html')

                elif text == 'Group status':
                    bot.sendMessage(chat_id, MEMBERS_ROLES)

                elif text == 'Hustlers list':
                    if user.role:
                        bot.sendMessage(chat_id, '\nMostly scams..\n')
                        for user in TelegramUser.objects.filter(role="Hustler"):
                            bot.sendMessage(chat_id, f'{user.name()} id_{user.telegram_id} {user.get_role_display()}')
                    else:
                        bot.sendMessage(chat_id, SERV_MSG[1])
                elif text == 'Market news':
                    if user.role:
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
                    if user.role is not None and user.role not in ['Member']:
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
                    bot.sendMessage(chat_id, text='appreciated that 😉, check there',
                                    reply_markup=InlineKeyboardMarkup.a(
                                        inline_keyboard=[[InlineKeyboardButton.a('Rules & more',
                                                                                 url='https://altcoinwhales.com/rules/')]]))

                elif text == 'Channel':
                    bot.sendMessage(chat_id,
                                    "Go to @altcoinwhales\n\nCharts from channel admins 🐳:\n➖Artem\n➖Excavo\n➖RocketBomb\n➖LA440\n➖Liquidity Hunter\n➖Edward Morra\n➖Crypto Cove\n& more...\n",
                                    reply_markup=InlineKeyboardMarkup.a(
                                        inline_keyboard=[[InlineKeyboardButton.a('Go', url='t.me/altcoinwhales')]]))

                elif text == 'Active users':
                    n = TelegramUser.objects.filter(updated_at__gte=now() - timedelta(hours=24)).count()
                    bot.sendMessage(chat_id, f'🌐 <b>{n}</b> users are currently active', parse_mode="html")

                elif text == 'Quote':
                    if user.role is not None and user.role not in ['Member']:
                        quote = random.choices(QUOTES_STRINGS)
                        bot.sendMessage(chat_id, {quote[0]}, parse_mode="html")
                    else:
                        bot.sendMessage(chat_id, SERV_MSG[1])

                elif text == "Market trend":
                    if user.role is not None and user.role not in ['Member']:
                        cap = requests.get(url='https://api.coingecko.com/api/v3/global')
                        fear = requests.get(url='https://api.alternative.me/fng/?limit=1')
                        tendency = requests.get(
                            url='https://api.cryptometer.io/trend-indicator-v3/?api_key=KLT7vnP42Bf4k55z07sA9ImHpVd2lN11s4B3854Y')
                        result_1 = cap.json()
                        result_2 = fear.json()
                        result_3 = tendency.json()
                        data = result_1["data"]
                        change = data["market_cap_change_percentage_24h_usd"]
                        btc = data["market_cap_percentage"]["btc"]
                        eth = data["market_cap_percentage"]["eth"]
                        change = round(change, 2)
                        change_price = '{:,}'.format(change)
                        btc = round(btc, 2)
                        domi_btc = '{:,}'.format(btc)
                        eth = round(eth, 2)
                        domi_eth = '{:,}'.format(eth)
                        data2 = result_2["data"][0]
                        feeling = data2["value_classification"]
                        number = data2["value"]
                        data3 = result_3["data"][0]
                        buy = data3["buy_pressure"]
                        sell = data3["sell_pressure"]
                        score = data3["trend_score"]
                        buy = round(buy)
                        sell = round(sell)
                        score = round(score)
                        score = get_tendency(score)
                        total = f'📊 <b>24h market change:</> {change_price}%\n▪️<b>BTC</> dom: {domi_btc}%\n▪️<b>ETH</> dom: {domi_eth}%\n\n' \
                                f'〽️<b>Last 4h trend:</> {score}\n🐮 {buy}%\n🐻 {sell}%\n\n' \
                                f'😵 {feeling} ({number}/100)'
                        bot.sendMessage(chat_id, total, parse_mode='html')
                    else:
                        bot.sendMessage(chat_id, SERV_MSG[1])

                elif text == '/start':
                    bot.sendMessage(chat_id, "🟠 start the bot from the group")

                elif text == '/up' or text == '/up@AltBabybot' or text == '/up@AltFishBot':
                    bot.sendMessage(chat_id, SERV_MSG[2])

                else:
                    bot.sendMessage(chat_id, SERV_MSG[3])