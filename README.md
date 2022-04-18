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
 + ** Info** - help message
 + **Faucet **- gives (faucet) 20k coins to your account\wallet
    * **Repeate Faucet** - repeate faucet for current address\wallet (including with the address from the context)
        > After entering the address for the first time, the address enters the context, which means that you can use the “Repeat Faucet” function without additional address entry.
    * **Main Menu** - Back to Main Menu
 + ** Wallet Menu** - Wallet Menu.
    *  **New Wallet** - Generate New Wallet, with:
        * Mnemonic phrase (24 words, BIP39)
        * Address
        * Auth key
        * Public key
        * Private Key
        > After generating a new wallet, the address of the new wallet gets into the context, which means that you can find out information about the wallet and also use the "Faucet" function without additionally entering the address.
    * **Private Key to Address** - Generates wallet Address from Private key
        * Back to Wallet Menu - Back to Wallet Menu
    * **Generates 24 words from your PK (BIP39)** - Generates 24 words from your PK (BIP39)
        * **Back to Wallet Menu** - Back to Wallet Menu
    * **Wallet info **- Info about your wallet
        * **Back to Wallet Menu** - Back to Wallet Menu
    * **Main Menu** - Back to Main Menu


Power by aiogram.