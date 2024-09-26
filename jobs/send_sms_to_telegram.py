import telebot
# from telegram import Bot
from aiogram import Bot, exceptions
import asyncio
from .config import *



bot = telebot.TeleBot(BOT_TOKEN)

async def send_message_to_group(bot_token, group_id, message):
    bot = Bot(token=bot_token)
    try:
        text = message.get('text')
        await bot.send_message(chat_id=group_id, text=text)
        print('Сообщение успешно отправлено в группу!')
    except Exception as e:
        print(f'Произошла ошибка: {e}')

async def send_message_to_user(bot_token, username, message):
    async with Bot(token=bot_token) as bot:
        try:
            text = message.get('text')
            await bot.send_message(chat_id=int(username), text=text)
            print('Сообщение успешно отправлено пользователю!')
        except exceptions.TelegramAPIError as e:
            if "chat not found" in str(e).lower():
                print(f'Произошла ошибка: Chat not found для пользователя @{username}')
            else:
                print(f'Произошла ошибка: {e}')
        except Exception as e:
            print(f'Произошла ошибка: {e}')


def send_sms_to_telegram(bot_token, chat_id_or_username, message,text):
    if text == 'group':
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(send_message_to_group(bot_token, chat_id_or_username, message))
    elif text == 'user':
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(send_message_to_user(bot_token, chat_id_or_username, message))
    else:
        print("Ошибка: Неверное значение параметра 'text'. Используйте 'group' или 'user'.")