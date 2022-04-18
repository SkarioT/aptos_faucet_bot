from aiogram.types import KeyboardButton,ReplyKeyboardMarkup#,InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardRemove

# --- MAIN MENU --- 
btnInfo = KeyboardButton("Info")
btnFaucet = KeyboardButton("Faucet")
btnWalletMenu = KeyboardButton("Wallet Menu")
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo,btnFaucet,btnWalletMenu)

btnBackToMainMenu = KeyboardButton("Main Menu")

# --- FAUCET ---
btnRepeateFaucet = KeyboardButton("Repeate Faucet")
faucetMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnRepeateFaucet,btnBackToMainMenu)


# --- WALLEN MENU ---
btnNewWallet = KeyboardButton("New Wallet")
btnAdressFromPK = KeyboardButton("Private Key to Address")
btnMnemonicFromPK = KeyboardButton("Generates 24 words from your PK (BIP39)")
btnWalletInfo = KeyboardButton("Wallet info")
btnBackToWalletMenu = KeyboardButton("Back to Wallet Menu")
adfpkMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnBackToWalletMenu)


walletMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnNewWallet,btnAdressFromPK,btnMnemonicFromPK,btnWalletInfo,btnBackToMainMenu)



