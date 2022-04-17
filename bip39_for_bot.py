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

    print("Address: ",new_acc.address())
    print("Auth_key: ",new_acc.auth_key())
    print("Public_key: ",new_acc.pub_key())
    print("Private_key: ",hex_private_key)
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
# generate_mnemonic_from_pk(get_address_from_pk("75bec726d02fbd825dd6a14ac864b526e7ff6b0297f91404a751f218577c4585"))

# print(len("75bec726d02fbd825dd6a14ac864b526e7ff6b0297f91404a751f218577c4585"))
# mpk = "48CC865EE4EECCB8DB584CF07C177F42E9D5A73905AA174576ECB3DF00999554"
# print(get_address_from_pk(mpk))
