from datetime import datetime
from os import stat
from aiogram import Bot,Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from auth_data import token
import asyncio

from aiogram import types
from aiogram.types import KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from aiogram import executor

from faucet_logic import faucet_client,rest_client


import time

bot = Bot(token)
dp = Dispatcher(bot,storage=MemoryStorage())

from aiogram.dispatcher.filters.state import State,StatesGroup

class GameStates(StatesGroup):
    default = State()
    start = State()
    faucet = State()
    balance = State()


welcome_msg = "Hi!\n  БОТ позволяет получить 1000 монет на Ваш аккаунт. Список доступных команд:\n/help - возвращет данное сообщение\n/faucet - Выдаёт на Ваш аккаунт 1к монет"

@dp.message_handler(commands=['start'],state="*")
async def send_welcome(message: types.Message,state: FSMContext):
    state_bot = await state.get_state()
    print(state_bot)
    if 'start' in str(state_bot):
        bad_answer = await message.reply(f"Невозможно повторно запустить бот. Бот уже запущен!\n /help - информация по командам бота")
        time.sleep(5)
        await bad_answer.delete()
    else:
        answer = await bot.send_message(message.from_user.id,welcome_msg)
        await GameStates.start.set()
    await message.delete()
    state_bot = await state.get_state()
    print(state_bot)

@dp.message_handler(commands=['help'],state="*")
async def send_welcome(message: types.Message,state: FSMContext):
    answer = await bot.send_message(message.from_user.id,welcome_msg)
    await GameStates.start.set()
    await message.delete()
    
@dp.message_handler(commands=['balance'],state="*")
async def send_welcome(message: types.Message,state: FSMContext):
    await GameStates.balance.set()
    answer_msg = await bot.send_message(message.from_user.id,f"Вы выбрали просмотр баланса своего аккаунта\nВведите адресс вашего Аккунта:")
    #msg_text = message.text
    # balance = await message.reply(f"Your current balance: {rest_client.account_balance(msg_text)}\nEnter /help for change address")
    await asyncio.sleep(10)
    await answer_msg.delete()
    await message.delete()
    
@dp.message_handler(state=GameStates.balance)
async def send_welcome(message: types.Message,state: FSMContext):
    msg_text = message.text
    print(msg_text,message.from_user.username,datetime.now())
    msg_for_clients = await message.reply(f"You entered: {msg_text}")
    if len(msg_text)!=64:
        print("хуету ввел")
        bad_msg = await message.reply("Bad address =( \n Address length must be 64 !!!")
        await asyncio.sleep(5)
        await bad_msg.delete()
        await msg_for_clients.delete()
    else:
        balance = await bot.send_message(message.from_user.id,f"Your current balance: {rest_client.account_balance(msg_text)}\nEnter /help for change address")
        await asyncio.sleep(5)
        await msg_for_clients.delete()
        await message.delete()
        await asyncio.sleep(5)
        #
        
    
    
    
    
@dp.message_handler(commands=['faucet'],state=GameStates.start)
async def send_welcome(message: types.Message,state: FSMContext):
    state_bot = await state.get_state()
    print(state_bot)
    await GameStates.faucet.set()
    bad_answer = await bot.send_message(message.from_user.id,f"Вы выбрали зачисление 1к момент на свой аккаунт\nВведите адресс вашего Аккунта:")
    await message.delete()

@dp.message_handler(state=GameStates.faucet)
async def send_welcome(message: types.Message,state: FSMContext):
    msg_text = message.text
    print(msg_text,message.from_user.username,datetime.now())
    msg_for_clients = await message.reply(f"You entered: {msg_text}")
    if len(msg_text)!=64:
        print("хуету ввел")
        bad_msg = await message.reply("Bad address =( \n Address length must be 64 !!!")
        await asyncio.sleep(5)
        await bad_msg.delete()
        await msg_for_clients.delete()
    else:
        faucet_client.fund_account(msg_text, 1000)
        balance = await bot.send_message(message.from_user.id,f"Your current balance: {rest_client.account_balance(msg_text)}\nEnter /help for change address")
        await asyncio.sleep(5)
        await msg_for_clients.delete()
        await message.delete()
        await asyncio.sleep(5)
        await balance.delete()

if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)