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


welcome_msg = "Hi!\n This BOT allows you to get 1000 coins to your account. List of available commands:\n/help - information about bot commands\n/faucet - Gives 1k coins to your account \n /balance - returns your wallet balance"

@dp.message_handler(commands=['start'],state="*")
async def send_welcome(message: types.Message,state: FSMContext):
    state_bot = await state.get_state()
    print(state_bot)
    if 'start' in str(state_bot):
        bad_answer = await message.reply(f"The bot cannot be re-started. The bot is already running!\n /help - information about bot commands")
        time.sleep(5)
        await bad_answer.delete()
    else:
        answer = await bot.send_message(message.from_user.id,welcome_msg)
        await GameStates.start.set()
    await message.delete()
    state_bot = await state.get_state()
    print(state_bot)

@dp.message_handler(commands=['help','change'],state="*")
async def send_welcome(message: types.Message,state: FSMContext):
    answer = await bot.send_message(message.from_user.id,welcome_msg)
    await GameStates.start.set()
    await message.delete()
    
    
# <----------- BALANCE LOGIC ---------------->    
@dp.message_handler(commands=['balance'],state="*")
async def send_welcome(message: types.Message,state: FSMContext):
    await GameStates.balance.set()
    answer_msg = await bot.send_message(message.from_user.id,f"You have chosen to view your account balance\nEnter your account\wallet address:")
    await asyncio.sleep(10)
    await message.delete()
    
        
# <----------- FAUCET LOGIC ---------------->      
@dp.message_handler(commands=['faucet'],state='*')
async def send_welcome(message: types.Message,state: FSMContext):
    state_bot = await state.get_state()
    print(state_bot)
    await GameStates.faucet.set()
    bad_answer = await bot.send_message(message.from_user.id,f"You have chosen to faucet 1,000 Moments to your account.\nEnter your account\wallet address:")
    await message.delete()

@dp.message_handler(state=GameStates.balance)
async def send_welcome(message: types.Message,state: FSMContext):
    msg_text = message.text
    print(msg_text,message.from_user,datetime.now())
    msg_for_clients = await message.reply(f"You entered: {msg_text}")
    if len(msg_text)!=64:
        print(f"Bad address =( {msg_text}\n Address length must be 64 chars !!!")
        bad_msg = await message.reply("Bad address =( \n Address length must be 64 chars !!!")
        await asyncio.sleep(5)
        await bad_msg.delete()
        await msg_for_clients.delete()
        await message.delete()
    else:
        balance = await bot.send_message(message.from_user.id,f"Your current balance: {rest_client.account_balance(msg_text)}\nEnter your address or any address again to request.")
        await asyncio.sleep(5)
        await msg_for_clients.delete()
        await message.delete()

@dp.message_handler(state=GameStates.faucet)
async def send_welcome(message: types.Message,state: FSMContext):
    msg_text = message.text
    print(msg_text,message.from_user,datetime.now())
    msg_for_clients = await message.reply(f"You entered: {msg_text}")
    if len(msg_text)!=64:
        print(f"Bad address =( {msg_text}\n Address length must be 64 chars !!!")
        bad_msg = await message.reply("Bad address =( \n Address length must be 64 chars!!!")
        await asyncio.sleep(5)
        await bad_msg.delete()
        await msg_for_clients.delete()
        await message.delete()
    else:
        faucet_client.fund_account(msg_text, 1000)
        balance = await bot.send_message(message.from_user.id,f"Your current balance: {rest_client.account_balance(msg_text)}\nEnter your address or any address again to request.")
        await asyncio.sleep(5)
        await msg_for_clients.delete()
        await message.delete()
        await asyncio.sleep(5)
        await balance.delete()


#RUN
if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)