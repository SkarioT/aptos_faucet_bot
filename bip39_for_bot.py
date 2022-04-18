from mnemonic import Mnemonic   
from faucet_logic import Account
import bip39
from nacl.signing import SigningKey
import hashlib


def generate_new_wallet():
    mnemo = Mnemonic("english")
    words = mnemo.generate(strength=256)
    # print(words)

    private_key = bip39.decode_phrase(words)
    new_acc = Account(private_key)
    hex_private_key = private_key.hex()

    data_return = {}
    data_return['mnemonic_24'] = words
    data_return['address'] = str(new_acc.address())
    data_return['auth_key'] = new_acc.auth_key()
    data_return['public_key'] = new_acc.pub_key()
    data_return['private_key'] = hex_private_key
    return data_return
    
    
def generate_mnemonic_from_pk(address):
    back = bip39.encode_bytes(bytes.fromhex(address)) 
    print("mnemonic from Private Key:\n")
    print(back)
    return back

#:!:>section_3
def get_address_from_pk(pk):
    signing_key = SigningKey(bytes.fromhex(pk))
    hasher = hashlib.sha3_256()
    hasher.update(signing_key.verify_key.encode() + b'\x00')
    address_from_pk =hasher.hexdigest()
    return address_from_pk
#<:!:section_3
