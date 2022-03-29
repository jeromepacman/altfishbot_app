import requests
import json
import time
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
from .quotes import QUOTES_STRINGS, TRADE_STRINGS, MEMBERS_ROLES
from .helpers import get_tendency


# commands #########


# Internal direct requests #######################
@processor(state_manager, from_states=state_types.All, message_types=[message_types.Text],
           update_types=update_types.Message)
def post_count(bot: TelegramBot, update: Update, state: TelegramState):
    chat_type = update.get_chat().get_type()
    text = update.get_message().get_text()
    user_id = update.get_user().get_id()

    if chat_type == 'supergroup' and len(text) >= 5 and not text.startswith('/'):
        a = TelegramUser.objects.get(telegram_id=user_id)
        a.post_count += 1
        a.updated_at = now()
        a.save()


#  requests #######################
@processor(state_manager, from_states=state_types.All, message_types=[message_types.Text],
           update_types=update_types.Message)
def quotes(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    text = update.get_message().get_text()
    user_id = update.get_user().get_id()

    if text == '/quote':
        quote = random.choices(QUOTES_STRINGS)
        bot.sendMessage(chat_id, {quote[0]}, parse_mode="html")

    elif text.startswith('$trade '):
        if len(text) > 8 and (text[7:]).isupper:
            quote = random.choices(TRADE_STRINGS)
            bot.sendMessage(chat_id, quote[0])
        else:
            bot.sendMessage(chat_id, text == 'I dont get it, I need the acronym of the ponzi')

    elif text == '/active':
        n = TelegramUser.objects.filter(updated_at__gte=now() - timedelta(hours=24)).count()
        bot.sendMessage(user_id, f'🌐 <b>{n}</b> users are currently active', parse_mode="html")

    elif text == '/db':
        try:
            TelegramUser.objects.filter(has_status=False).delete()
        except:
            bot.sendMessage(chat_id='342785208', text="Data failed")
        else:
            bot.sendMessage(chat_id='342785208', text="Data purged")


@processor(state_manager, from_states=state_types.All, message_types=message_types.Text,
           update_types=update_types.Message)
def role(bot: TelegramBot, update: Update, state: TelegramState):
    text = update.get_message().get_text()
    user_id = update.get_user().get_id()
    user_name = update.get_message().get_from()
    chat_id = update.get_chat().get_id()
    sender = update.get_message().get_reply_to_message()
    if text == '/who':
        if sender is not None:
            hook = sender.get_from().get_id()
            a = TelegramUser.objects.get(telegram_id=hook)
            if a.role is not None:
                response = f'Hey {user_name.first_name}\n{a} is {a.get_role_display()}'
                bot.sendMessage(chat_id, response)
            else:
                bot.sendMessage(chat_id, 'no status found')

    elif text == '/inf':
        b = TelegramUser.objects.get(telegram_id=user_id)
        if b.role is not None:
            c = f'{b.get_role_display()}'
            bot.sendMessage(chat_id, f'Hi {b.first_name} 😎\nYour Status: \n{c}')
        else:
            bot.sendMessage(chat_id, f"😶 You don't have any status {b.first_name}")


@processor(state_manager, from_states=state_types.Reset, message_types=message_types.Text,
           update_types=update_types.Message)
def promote(bot: TelegramBot, update: Update, state: TelegramState):
    text = update.get_message().get_text()
    user_id = update.get_user().get_id()
    chat_id = update.get_chat().get_id()
    sender = update.get_message().get_reply_to_message()
    if text == '/promote' and user_id == '342785208':
        if sender is not None:
            hook = sender.get_from().get_id()
            a = TelegramUser.objects.get(telegram_id=hook)
            if a.role is not None:
                response = f'▫️{a} got a new status:\n▫️    ➖ {a.get_role_display()}  ➖  '
                bot.sendMessage(chat_id, response)
        else:
            bot.sendMessage(chat_id, 'Bad request')


@processor(state_manager, from_states=state_types.All, message_types=message_types.Text, update_types=update_types.Message)
def trendy(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    text = update.get_message().get_text()
    if text == '/top':
        request = requests.get(url='https://api.coingecko.com/api/v3/search/trending')
        result = request.json()
        coins = result["coins"][:5]
        url = f'https://coingecko.com/coins/'
        bot.sendMessage(chat_id, text='📈 Trending coins searched on Gecko:', parse_mode='html')
        for x in coins:
            symbol = x["item"]["symbol"]
            num = x["item"]["slug"]
            response = f'➖ <a href="{url}{num}">{symbol}</a>'
            bot.sendMessage(chat_id, response, disable_web_page_preview=True, parse_mode='html')

    elif text == "/cap":
        cap = requests.get(url='https://api.coingecko.com/api/v3/global')
        fear = requests.get(url='https://api.alternative.me/fng/?limit=1')

        tendency = requests.get(url='https://api.cryptometer.io/trend-indicator-v3/?api_key=KLT7vnP42Bf4k55z07sA9ImHpVd2lN11s4B3854Y')
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

    elif text == "/news":
        news = requests.get(url='https://min-api.cryptocompare.com/data/v2/news/?lang=EN')
        api = news.json()
        data = api["Data"][:5]
        for x in data:
            title = x["title"]
            url = x["url"]
            source = x["source"]
            response = f'🌎{source.title()}\n<a href="{url}">{title}</a>'
            bot.sendMessage(chat_id, {response}, disable_web_page_preview=True, parse_mode='html')


# Private chat actions  #######################
@processor(state_manager, from_states=state_types.All, message_types=message_types.Text,
           update_types=update_types.Message)
def team_ask(bot: TelegramBot, update: Update, state: TelegramState):
    chat_type = update.get_chat().get_type()
    text = update.get_message().get_text()
    chat_id = update.get_chat().get_id()
    if chat_type == 'private':
        if text == '/adminlist':
            bot.sendMessage(chat_id, 'chat - Active admins')
            for a in TelegramUser.objects.filter(role='Admin'):
                if not a.is_bot:
                    bot.sendMessage(chat_id, f' @{a.username} {a.get_role_display()}')
        elif text == '/scamlist':
            bot.sendMessage(chat_id, f'Mostly scams...')
            for a in TelegramUser.objects.filter(role="Hustler"):
                bot.sendMessage(chat_id, f'{a.name()} #id{a.telegram_id} {a.get_role_display()}')
        elif text == '/insiderlist':
            for a in TelegramUser.objects.filter(role="Dolphin"):
                bot.sendMessage(chat_id, f'{a.name_gen()} {a.get_role_display()}')
            for a in TelegramUser.objects.filter(role="Babywhale"):
                bot.sendMessage(chat_id, f'{a.name_gen()} {a.get_role_display()}')
            bot.sendMessage(chat_id,
                            text='<i>Your current status does not allow you to access the list of top level members</>',
                            parse_mode='html')


@processor(state_manager, from_states=state_types.All, message_types=message_types.Text,
           update_types=update_types.Message)
def welcome(bot: TelegramBot, update: Update, state: TelegramState):
    chat_direct = update.get_message().get_from().get_id()
    text = update.get_message().get_text()

    if text == '/up' or text == '/up@AltBabybot' or text == '/up@AltFishBot':
        bot.sendMessage(
            chat_direct,
            text='Hi there, wanna check some stuff ?',
            reply_markup=ReplyKeyboardMarkup.a(resize_keyboard=True, keyboard=[
                [KeyboardButton.a('My status'), KeyboardButton.a('Admins list')],
                [KeyboardButton.a('Status'), KeyboardButton.a('Hustlers list')],
                [KeyboardButton.a('News'), KeyboardButton.a('Gecko trend coins')],
                [KeyboardButton.a('Rules of the group'), KeyboardButton.a('Channel')],
            ])
        )


@processor(state_manager, from_states=state_types.All, message_types=message_types.Text,
           update_types=update_types.Message)
def resp_kb(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    text = str(update.get_message().get_text())
    chat_type = update.get_chat().get_type()
    if chat_type == 'private':
        if text == 'My status':
            b = TelegramUser.objects.get(telegram_id=chat_id)
            if b.role is not None:
                c = f'{b.get_role_display()}'
                bot.sendMessage(chat_id, f"Hi {b.first_name} 😎\n\nYour Status is {c}\n\nYou're in the group since {b.joined}\n\n Date may be incorrect, i'm still in beta")
            else:
                bot.sendMessage(chat_id, f"😶 You don't have any status")

        elif text == 'Admins list':
            bot.sendMessage(chat_id, 'chat - Active admins')
            for a in TelegramUser.objects.filter(role='Admin'):
                if not a.is_bot:
                    bot.sendMessage(chat_id, f' @{a.username} {a.get_role_display()}')

        elif text == 'Status':
            bot.sendMessage(chat_id, MEMBERS_ROLES)

        elif text == 'Hustlers list':
            bot.sendMessage(chat_id, f'Mostly scams...')
            for a in TelegramUser.objects.filter(role="Hustler"):
                bot.sendMessage(chat_id, f'{a.name()} #id{a.telegram_id} {a.get_role_display()}')

        elif text == 'News':
            news = requests.get(url='https://min-api.cryptocompare.com/data/v2/news/?lang=EN')
            api = news.json()
            data = api["Data"][:7]
            for x in data:
                title = x["title"]
                url = x["url"]
                source = x["source"]
                response = f'🌎{source.title()}\n<a href="{url}">{title}</a>'
                bot.sendMessage(chat_id, {response}, disable_web_page_preview=True, parse_mode='html')

        elif text == 'Gecko trend coins':
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

        elif text == 'Rules of the group':
            bot.sendMessage(chat_id, text='appreciated that 😉, check there', reply_markup=InlineKeyboardMarkup.a(inline_keyboard=[[InlineKeyboardButton.a('Rules & more', url='https://altcoinwhales.com/rules/')]]))

        elif text == 'Channel':
            bot.sendMessage(chat_id,
                            "Go to @altcoinwhales\n\nCharts from channel admins 🐳:\n➖Artem\n➖Rocketbomb\n➖LA440\n➖Liquidity Hunter\n➖Excavo\n➖Edward Morra\n➖Jerome\n& more...\n",
                            reply_markup=InlineKeyboardMarkup.a(
                                inline_keyboard=[[InlineKeyboardButton.a('Go', url='t.me/altcoinwhales')]]))

        elif text == '/up' or text == '/up@AltBabybot' or text == '/up@AltFishBot':
            bot.deleteMessage(chat_id, update.get_message())

        else:
            bot.sendMessage(chat_id, 'I didn\'t get that! Use the keyboard below')


