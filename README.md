### Features

Bot for faucet 20k coins on the Aptos (dev) blockchain and checking the balance.

Bot address/name:
t.me/aptos_faucet_bot

Old Commands:
 - /help - help message
 - /balance - check your balance
 - /faucet - gives (faucet) 20k coins to your account\wallet
 - /address - generates wallet address from private key

New commands ( button):
 + **β Info** - help message
 + **π° Faucet**- gives (faucet) 20k coins to your account\wallet
    * **π° Repeate Faucet** - repeate faucet for current address\wallet (including with the address from the context)
        > πAfter entering the address for the first time, the address enters the context, which means that you can use the βRepeat Faucetβ function without additional address entry.
    * **π Main Menu** - Back to Main Menu
 + **β‘οΈ Wallet Menu** - Wallet Menu.
    *  **π¨ New Wallet** - Generate New Wallet, with:
        * π Mnemonic phrase (24 words, BIP39)
        * π Address
        * π Auth key
        * π Public key
        * π Private Key
        > πAfter generating a new wallet, the address π of the new wallet gets into the context, which means that you can find out information about the wallet and also use the "Faucet" function without additionally entering the address.
    * **πβ‘οΈπ PK to Address|pub_key** - Getting wallet Address and Public Key from Private key
        * **π Wallet Menu** - Back to Wallet Menu
    * **π Generates 24 words from your PK** - Generates 24 words from your PK (BIP39)
        * **π Wallet Menu** - Back to Wallet Menu
    * **βΉοΈ Wallet info**- Info about your wallet
        * **π Wallet Menu** - Back to Wallet Menu
    * **π Main Menu** - Back to Main Menu


Power by aiogram.