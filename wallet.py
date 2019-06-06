from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii #convert binary to ascii

class Wallet:
    def __init__(self, node_id):
        self.private_key = None
        self.public_key = None
        self.node_id = node_id

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key


    def save_keys(self):
        try:
            with open('wallet-{}.txt'.format(self.node_id), mode = 'w') as file:
                file.write(self.public_key)
                file.write('\n')
                file.write(self.private_key)
                return True 
        except IOError:
            print("Error !!! Saving wallet")
            return False


    def load_keys(self):
        try:
            with open('wallet-{}.txt'.format(self.node_id), mode = 'r') as file:
                keys = file.readlines()
                self.public_key = keys[0][:-1]
                self.private_key = keys[1]
                return True
        except IOError:
            print("Error !!! Loading keys from wallet")
            return False


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