from aiogram.types import KeyboardButton,ReplyKeyboardMarkup

# --- MAIN MENU --- 
btnInfo = KeyboardButton("â Info")
btnFaucet = KeyboardButton("đ° Faucet")
btnWalletMenu = KeyboardButton("âĄī¸ Wallet Menu")
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo,btnFaucet,btnWalletMenu)

btnBackToMainMenu = KeyboardButton("đ Main Menu")

# --- FAUCET ---
btnRepeateFaucet = KeyboardButton("đ° Repeate Faucet")
faucetMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnRepeateFaucet,btnBackToMainMenu)


# --- WALLEN MENU ---
btnNewWallet = KeyboardButton("đ¨ New Wallet")
btnAdressFromPK = KeyboardButton("đâĄī¸đ PK to Address|Public Key")
btnMnemonicFromPK = KeyboardButton("đ Generates 24 words from your PK")
btnWalletInfo = KeyboardButton("âšī¸ Wallet info")
btnBackToWalletMenu = KeyboardButton("đ Wallet Menu")
adfpkMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnBackToWalletMenu)


walletMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnNewWallet,btnAdressFromPK,btnMnemonicFromPK,btnWalletInfo,btnBackToMainMenu)



