from aiogram.types import KeyboardButton,ReplyKeyboardMarkup

# --- MAIN MENU --- 
btnInfo = KeyboardButton("❓ Info")
btnFaucet = KeyboardButton("🚰 Faucet")
btnWalletMenu = KeyboardButton("➡️ Wallet Menu")
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo,btnFaucet,btnWalletMenu)

btnBackToMainMenu = KeyboardButton("🔙 Main Menu")

# --- FAUCET ---
btnRepeateFaucet = KeyboardButton("🚰 Repeate Faucet")
faucetMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnRepeateFaucet,btnBackToMainMenu)


# --- WALLEN MENU ---
btnNewWallet = KeyboardButton("🖨 New Wallet")
btnAdressFromPK = KeyboardButton("🔐➡️🗝 PK to Address")
btnMnemonicFromPK = KeyboardButton("📝 Generates 24 words from your PK")
btnWalletInfo = KeyboardButton("ℹ️ Wallet info")
btnBackToWalletMenu = KeyboardButton("🔙 Wallet Menu")
adfpkMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnBackToWalletMenu)


walletMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnNewWallet,btnAdressFromPK,btnMnemonicFromPK,btnWalletInfo,btnBackToMainMenu)



