import asyncio
import logging
from time import sleep

from aiogram import Bot, Dispatcher, executor
from aiogram import types

from admin_filter import MyFilter
from config import *
from db1 import DB
from texts import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

admins = [1991258107]
rank = 3
rank_name = 'новокек'
chat_id = 0
rep = 0

db = DB()

dp.filters_factory.bind(MyFilter)


@dp.message_handler(is_admin=True, commands=["бан", 'ban'], commands_prefix='!/')
async def kick(message: types.Message):
    if message.reply_to_message:
        await message.bot.kick_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        await message.reply_to_message.reply(
            f'<a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a> Заблокирован',
            parse_mode='HTML')
    elif not message.reply_to_message:
        await message.reply('Команда должна быть ответом на сообщение!')


@dp.message_handler(content_types='new_chat_member')
async def newmember(message: types.Message):
    await message.delete()


@dp.message_handler(commands=["infa", 'инфа'], commands_prefix='!/')
async def infa(message: types.Message):
    global rank, rank_name, rep
    if message.reply_to_message == None:
        db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
                    message.from_user.last_name, rank, rank_name, chat_id=message.chat.id, rep=rep)
        await message.reply(f"""💗Ваш инфа {message.from_user.get_mention(as_html=True)}: 💗 
🆔ID:{message.from_user.id} 🆔
🔅Username: @{message.from_user.username} 🔅
🌀Имя: {message.from_user.first_name} | {message.from_user.last_name}🌀
💼Ранг: {db.get_rank1(str(message.from_user.id))}💼
🏆Репутация: {db.get_rep(str(message.from_user.id))}🏆""", parse_mode='HTML')
    if message.reply_to_message:
        db.add_user(message.reply_to_message.from_user.id, message.reply_to_message.from_user.username,
                    message.reply_to_message.from_user.first_name,
                    message.reply_to_message.from_user.last_name, rank, rank_name, chat_id=message.chat.id, rep=rep)
        await message.reply(f"""💗 инфа {message.reply_to_message.from_user.get_mention(as_html=True)}: 💗 
🆔ID:{message.reply_to_message.from_user.id} 🆔
🔅Username: @{message.reply_to_message.from_user.username} 🔅
🌀Имя: {message.reply_to_message.from_user.first_name} | {message.reply_to_message.from_user.last_name}🌀
💼Ранг: {db.get_rank1(str(message.reply_to_message.from_user.id))}💼
🏆Репутация: {db.get_rep(str(message.reply_to_message.from_user.id))}🏆""", parse_mode='HTML')


@dp.message_handler(commands=["сетранг", 'setrank'], commands_prefix='!/', is_reply=True)
async def setrank(message: types.Message):
    global rank, rank_name, rep, chat_id, admins
    rank = int(message.get_args())
    chat_id = message.chat.id
    if message.from_user.id in admins:
        if message.reply_to_message.from_user.id in admins:
            await message.reply('Админы вне рангов')
        else:
            if type(rank) == int:
                if rank <= 10 and rank >= 1:
                    if rank < 3 and rank >= 1:
                        rank_name = 'клоун'
                        await message.reply(
                            f"@{message.reply_to_message.from_user.username}({message.reply_to_message.from_user.id}) - изменен ранг на '{rank}' | {rank_name}")
                        db.update_rank(message.reply_to_message.from_user.id, rank)
                    elif rank < 5 and rank >= 3:
                        rank_name = 'новокек'
                        await message.reply(
                            f"@{message.reply_to_message.from_user.username}({message.reply_to_message.from_user.id}) - изменен ранг на '{rank}' | {rank_name}")
                        db.update_rank(message.reply_to_message.from_user.id, rank)
                    elif rank < 7 and rank >= 5:
                        rank_name = 'дефолт'
                        await message.reply(
                            f"@{message.reply_to_message.from_user.username}({message.reply_to_message.from_user.id}) - изменен ранг на '{rank}' | {rank_name}")
                        db.update_rank(message.reply_to_message.from_user.id, rank)
                    elif rank < 9 and rank >= 7:
                        rank_name = 'норм чел'
                        await message.reply(
                            f"@{message.reply_to_message.from_user.username}({message.reply_to_message.from_user.id}) - изменен ранг на '{rank}' | {rank_name}")
                        db.update_rank(message.reply_to_message.from_user.id, rank)
                    elif rank >= 9 and rank < 11:
                        rank_name = 'спонсор'
                        await message.reply(
                            f"@{message.reply_to_message.from_user.username}({message.reply_to_message.from_user.id}) - изменен ранг на '{rank}' | {rank_name}")
                        db.update_rank(message.reply_to_message.from_user.id, rank)
                else:
                    await message.reply(
                        f'Ранг от 1 до 10')
            else:
                await message.reply('Ранг от 1 до 10!')
    else:
        await message.reply('Вы не админ')

    db.add_user(message.reply_to_message.from_user.id, message.reply_to_message.from_user.username,
                message.reply_to_message.from_user.first_name,
                message.reply_to_message.from_user.last_name, rank, rank_name, chat_id=message.chat.id, rep=rep)


@dp.message_handler(commands=["repost", 'рассылка'], commands_prefix='!/')
async def repost(message: types.Message):
    repost = message.get_args().split()[1:]
    ss = ' '.join(repost)
    aa = int(message.get_args().split()[0])
    if message.from_user.id in admins:
        while aa > 0:
            if aa >= 10:
                await message.reply('нельзя столько')
                break
            else:
                aa -= 1
                await asyncio.sleep(1)
                await message.answer(ss)
    else:
        await message.reply('Вы не админ')


@dp.message_handler(is_reply=True)
async def reputation(message: types.Message):
    global rep
    if message.text == '+':
        db.add_user(message.reply_to_message.from_user.id, message.reply_to_message.from_user.username,
                    message.reply_to_message.from_user.first_name,
                    message.reply_to_message.from_user.last_name, rank, rank_name, chat_id=message.chat.id, rep=rep)
        rep += 1
        await message.answer(
            f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> повысил <a href="tg://user?id={message.reply_to_message.from_user.id}">ему</a> на +1',
            parse_mode='HTML')
        db.add_rep(rep, message.reply_to_message.from_user.id)
    if message.text == '-':
        db.add_user(message.reply_to_message.from_user.id, message.reply_to_message.from_user.username,
                    message.reply_to_message.from_user.first_name,
                    message.reply_to_message.from_user.last_name, rank, rank_name, chat_id=message.chat.id, rep=rep)
        rep -= 1
        await message.answer(
            f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> понизил <a href="tg://user?id={message.reply_to_message.from_user.id}">ему</a> на -1',
            parse_mode='HTML')
        db.add_rep(rep, message.reply_to_message.from_user.id)


@dp.message_handler(commands=["alt_repost", 'альт_рассылка'], commands_prefix='!/')
async def repost1(message: types.Message):
    repost1 = message.get_args().split()[1:]
    ss1 = ' '.join(repost1)
    aa1 = int(message.get_args().split()[0])
    if message.from_user.id in admins:
        if aa1 <= 20:
            await message.reply('Слишком маленький промежуток!')
        else:
            while True:
                sleep(aa1)
                await message.answer(ss1)
    else:
        await message.reply('Вы не админ')


@dp.message_handler(commands=["getop", 'топ'], commands_prefix='!/')
async def top(message: types.Message):
    db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
                message.from_user.last_name, rank, rank_name, chat_id=message.chat.id, rep=rep)
    await message.reply(f'Топ юзеров: \n {db.get_top()}', parse_mode='HTML')


@dp.message_handler(commands=["reptop", 'рептоп'], commands_prefix='!/')
async def top1(message: types.Message):
    db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
                message.from_user.last_name, rank, rank_name, chat_id=message.chat.id, rep=rep)
    await message.reply(f'Топ юзеров: \n {db.global_rep()}', parse_mode='HTML')


@dp.message_handler(commands="start", commands_prefix='!/')
async def start(message: types.Message):
    db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
                message.from_user.last_name, rank, rank_name, chat_id=message.chat.id, rep=rep)
    await message.answer(
        f'Привет, <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>! Напиши /help,чтобы узнать что я умею',
        parse_mode="HTML")


@dp.message_handler(commands=["хелп", 'help'], commands_prefix='!/')
async def help(message: types.Message):
    db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
                message.from_user.last_name, rank, rank_name, chat_id=message.chat.id, rep=rep)
    await message.reply(help_text)


@dp.message_handler(commands=["мойранг", 'myrank'], commands_prefix='!/')
async def ranks(message: types.Message):
    db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
                message.from_user.last_name, rank, rank_name, chat_id=message.chat.id, rep=rep)
    await message.reply(f'Ваш ранг: \n {db.get_rank(str(message.from_user.id))}')


@dp.message_handler()
async def da_net(message: types.Message):
    for texts in da:
        if texts == message.text:
            await message.reply('пизда')
    for net_text in net:
        if net_text == message.text:
            await message.reply('пидора ответ')


@dp.message_handler()
async def filter(message: types.Message):
    for text in sss:
        if text in message.text and message.from_user.id not in admins:
            await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
