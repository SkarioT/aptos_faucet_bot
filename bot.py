from aiogram import Bot,Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram import executor
from aiogram.dispatcher.filters.state import State,StatesGroup

from faucet_logic import faucet_client,rest_client
from bip39_for_bot import generate_new_wallet,get_address_from_pk,generate_mnemonic_from_pk
from auth_data import token
import bot_btn_menu as navigation


import asyncio

bot = Bot(token)
dp = Dispatcher(bot,storage=MemoryStorage())



class MenuStates(StatesGroup):
    default = State()
    start = State()
    faucet = State()
    afpk = State()
    wallet = State()
    seed24 = State()

welcome_msg ="""
❓ Info  - help message
🚰 Faucet - gives (faucet) 20k coins to your account\wallet
    🚰 Repeate Faucet  - repeate faucet for current address\wallet (including with the address from the context)
        📜 After entering the address for the first time, the address enters the context, which means that you can use the “Repeat Faucet” function without additional address entry.
➡️ Wallet Menu  - Wallet Menu.
    🖨 New Wallet  - Generate New Wallet, with:
        📜 After generating a new wallet, the address 🗝 of the new wallet gets into the context, which means that you can find out information about the wallet and also use the "Faucet" function without additionally entering the address.
    🔐➡️🗝 PK to Address  - Generates wallet Address from Private key
    📝 Generates 24 words from your PK  - Generates 24 words from your PK (BIP39)
    ℹ️ Wallet info - Info about your wallet
    🔙 Main Menu  - Back to Main Menu
    
    Feed back: https://t.me/zhovy"""
async def get_status_menu(state):
    state_bot = await state.get_state()
    print(state_bot)

@dp.message_handler(state=None)
async def send_welcome(message: types.Message,state: FSMContext):
    answer = await bot.send_message(message.from_user.id,welcome_msg,reply_markup=navigation.mainMenu)
    await MenuStates.start.set()
    await message.delete()
    await get_status_menu(state)

@dp.message_handler(state=MenuStates.start)
async def menu(message: types.Message,state: FSMContext):
    print(message.text)
    if message.text == "❓ Info" or message.text == "/help" :
        ENG_msg_text_info = " You chose Info"
        await bot.send_message(message.from_user.id,ENG_msg_text_info)
        await bot.send_message(message.from_user.id,welcome_msg)
    elif message.text == "🚰 Faucet" or message.text == "/faucet":
        ENG_msg_text_info = "You chose 🚰 Faucet"
        await bot.send_message(message.from_user.id,ENG_msg_text_info)
        async with state.proxy() as data:
            if data.get('address'):
                await bot.send_message(message.from_user.id,f"Your current address 🗝 : {data.get('address')} Enter a new address for change",reply_markup=navigation.faucetMenu)
            else:
                await bot.send_message(message.from_user.id,"Enter your address 🗝 for 🚰 FAUCET 2️⃣0️⃣.0️⃣0️⃣0️⃣ coins :",reply_markup=navigation.faucetMenu)
        await MenuStates.faucet.set()
        await get_status_menu(state)
    elif message.text == "➡️ Wallet Menu" or message.text == "/balance" or message.text == "/address":
        RU_msg_text_wallet_menu = "You chose Wallet Menu"
        await bot.send_message(message.from_user.id,RU_msg_text_wallet_menu,reply_markup=navigation.walletMenu)
        await MenuStates.wallet.set()
        await get_status_menu(state)
    # else:
    #     await message.reply("I don't undartand. Plese press button:  ❓ Info",reply_markup=navigation.walletMenu)
        

# --- FAUCET ---
i=0 # for calculate counts faucet for address
@dp.message_handler(state=MenuStates.faucet)
async def get_faucet(message: types.Message,state: FSMContext):
    global i
    await get_status_menu(state)
    msg_text = message.text
    if msg_text == "🚰 Repeate Faucet":
        await message.delete()
        async with state.proxy() as data:
            print("data_in_repeate=",data)
            i+=1
            data['i']=i
            if data.get('address'): 
                msg_text = data.get('address')
                info_msg = f"You repeated 🎰 Faucet 🚰 {i} times for address {msg_text}"
                faucet_client.fund_account(msg_text, 20000)
                balance = await bot.send_message(message.from_user.id,f"Your current balance 💵 : {rest_client.account_balance(msg_text)}\n{info_msg}")
            else:
                info_msg = ''
    elif msg_text == "В главное меню" or msg_text == "🔙 Main Menu":
        await MenuStates.start.set()
        await bot.send_message(message.from_user.id,"🔛 Main Menu",reply_markup=navigation.mainMenu)
    elif len(msg_text)==64 or (len(msg_text)==66 and str(msg_text).startswith("0x") ) : #add start with "0x"
        i = 0
        async with state.proxy() as data:
            data['address'] = msg_text
            print("data=",data)
        faucet_client.fund_account(msg_text, 20000)
        balance = await bot.send_message(message.from_user.id,f"Your current balance 💵 : {rest_client.account_balance(msg_text)}")
    else:
        print(f"❌ Bad address =( {msg_text}\n Address length must be 64 chars !!!❌")
        bad_msg = await message.reply("❌ Bad address =( \n Address length must be 64 chars!!!❌")
        await asyncio.sleep(5)
        await bad_msg.delete()
        await message.delete()

# --- WALLEN MENU ---
@dp.message_handler(state=MenuStates.wallet)
async def get_faucet(message: types.Message,state: FSMContext):
    await get_status_menu(state)
    msg_text = message.text
    if msg_text == "🖨 New Wallet":
        new_wallet_data = generate_new_wallet()
        mnemonic_24 = new_wallet_data["mnemonic_24"]
        address = "0x" + new_wallet_data["address"]
        auth_key = "0x" + new_wallet_data["auth_key"]
        public_key = "0x" + new_wallet_data["public_key"]
        private_key = new_wallet_data["private_key"]
        await bot.send_message(message.from_user.id,f"📝 New Wallet mnemonic phrase (24 words, BIP39) :")
        await bot.send_message(message.from_user.id,mnemonic_24)
        await bot.send_message(message.from_user.id,f"🗝 New Wallet Address : ")
        await bot.send_message(message.from_user.id,f"{address}")
        await bot.send_message(message.from_user.id,f"🔑New Wallet Auth Key: {auth_key}")
        await bot.send_message(message.from_user.id,f"🔓New Wallet Public Key: {public_key}")
        await bot.send_message(message.from_user.id,f"🔐 New Wallet Private Key: ")
        await bot.send_message(message.from_user.id,f"{private_key}")
        async with state.proxy() as data:
            data['address'] = address
            data['i'] = 0
        
    elif msg_text == "🔐➡️🗝 PK to Address":
        await MenuStates.afpk.set()
        await get_status_menu(state)
        await bot.send_message(message.from_user.id,"Enter your 🔐 Private Key to get the address :",reply_markup=navigation.adfpkMenu)
    elif msg_text == "В главное меню" or msg_text == "🔙 Main Menu":
        await MenuStates.start.set()
        await bot.send_message(message.from_user.id,"Back to Main Menu",reply_markup=navigation.mainMenu)
    elif msg_text == "ℹ️ Wallet info":
        await bot.send_message(message.from_user.id,"🚧🔜 In development. Waint.",reply_markup=navigation.walletMenu)
    elif msg_text == "📝 Generates 24 words from your PK" or msg_text == "/mnemonic":
        await bot.send_message(message.from_user.id,"Enter your 🔐 Private Key to get the address :",reply_markup=navigation.adfpkMenu)
        await MenuStates.seed24.set()
    else:
        await bot.send_message(message.from_user.id,"Choose the correct menu item",reply_markup=navigation.walletMenu)
        
#  --- Address From PK ---
@dp.message_handler(state=MenuStates.afpk)
async def address_from_pk(message: types.Message,state: FSMContext):
    await get_status_menu(state)
    pk_from_msg = message.text
    print("pk_from_msg:",pk_from_msg)
    if pk_from_msg == "🔙 Wallet Menu":
        await MenuStates.wallet.set()
        await bot.send_message(message.from_user.id,"🔙 Wallet Menu",reply_markup=navigation.walletMenu)
    elif len(pk_from_msg)==64  : 
        address = "0x" + get_address_from_pk(pk_from_msg)
        async with state.proxy() as data:
            data['address'] = address
            print("data=",data)
        msg_address_info = await bot.send_message(message.from_user.id,f"Your 🗝 address from 🔐 Private key : ")
        msg_address = await bot.send_message(message.from_user.id,address)
        faucet_client.fund_account(address, 0)
        msg_balance = await bot.send_message(message.from_user.id,f"Your current balance 💵: {rest_client.account_balance(address)}")
    else:
        print(f"❌Bad Private Key =( {pk_from_msg}\n Private Key length must be 64 chars !!!❌")
        bad_msg = await message.reply("❌Bad Private Key =( \n Private Key length must be 64 chars!!!❌")
        await asyncio.sleep(5)
        await bad_msg.delete()
        await message.delete()

#  --- Generates 24 words from your PK ---
@dp.message_handler(state=MenuStates.seed24)
async def seed_words_from_pk(message: types.Message,state: FSMContext):
    await get_status_menu(state)
    pk_from_msg = message.text
    print("pk_from_msg:",pk_from_msg)
    if pk_from_msg == "🔙 Wallet Menu":
        await MenuStates.wallet.set()
        await bot.send_message(message.from_user.id,"🔙 Wallet Menu",reply_markup=navigation.walletMenu)
    elif len(pk_from_msg)==64  : 
        seed_24 = generate_mnemonic_from_pk(pk_from_msg)
        msg_address_info = await bot.send_message(message.from_user.id,f"Your 📝 24 words from 🔐 Private key : ")
        msg_address = await bot.send_message(message.from_user.id,seed_24)
    else:
        print(f"❌Bad Private Key =( {pk_from_msg}\n Private key length must be 64 chars !!!❌")
        bad_msg = await message.reply("❌Bad Private Key =( \n Private Key length must be 64 chars!!!❌")
        await asyncio.sleep(5)
        await bad_msg.delete()
        await message.delete() 

    
#RUN
if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)