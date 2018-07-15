from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii #convert binary to ascii

class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None


    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key


    def save_keys(self):
        try:
            with open('wallet.txt', mode = 'w') as file:
                file.write(self.public_key)
                file.write('\n')
                file.write(self.private_key)
        except IOError:
            print("Error !!! Saving wallet")


    def load_keys(self):
        try:
            with open('wallet.txt', mode = 'r') as file:
                keys = file.readlines()
                self.public_key = keys[0][:-1]
                self.private_key = keys[1]
        except IOError:
            print("Error !!! Loading keys from wallet")


    def generate_keys(self):
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), 
                binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))

            
    def sign_transactions(self, sender, recipient, amount):
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))
        h = SHA256.new((str(sender) + str(recipient) + str(amount)).encode('utf8'))
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_transactions(transaction):
        
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new((str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(transaction.signature))