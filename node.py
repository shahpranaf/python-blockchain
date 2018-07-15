from uuid import uuid4

from utility.verification import Verification
from blockchain import Blockchain
from wallet import Wallet

class Node:

    def __init__(self):
        #self.id = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)


    def get_transaction_value(self):
        tx_recipient = input("Enter the name of recipient: ")
        tx_amount = float(input("Please enter an amount: "))

        return tx_recipient, tx_amount

    
    def get_user_choice(self):
        return input("Your choice: ")

    
    def print_block_data(self):
        for block in self.blockchain.get_chain():
            print(block)

    
    def listen_user_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print('Please Choose')
            print('1. Add a new transaction value!')
            print('2. Mine the block')
            print('3. Print the block data')
            print('4. Check transaction validity')
            print('5. Create new wallet')
            print('6. Load Wallet')
            print('7. Save Wallet')
            print('q. Quit')
            user_choice = self.get_user_choice()

            if user_choice == '1':
                txn_data = self.get_transaction_value()
                recipient, amount = txn_data
                signature = self.wallet.sign_transactions(self.wallet.public_key, recipient, amount)

                if self.blockchain.add_transaction(recipient, self.wallet.public_key, signature, amount=amount):
                    print('Transaction Successfull')
                else:
                    print('Transaction Declined')

            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print("Mining Failed. Got no wallet?")

            elif user_choice == '3':
                self.print_block_data()

            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_balance, self.blockchain.get_open_transactions()):
                    print('All transactions are valid')
                else:
                    print('There are invalid transactions')
            
            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)

            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)

            elif user_choice == '7':
                self.wallet.save_keys()

            elif user_choice == 'q':
                waiting_for_input = False

            else:
                print("Input is not valid. Please select from the list!!")

            if not Verification.verify_chain(self.blockchain.chain):
                print('Invalid Blockchain')
                break

            # print(blockchain)

            # print(open_transactions)

            print(
                'Balance of {}: {:6.2f}'.format(self.wallet.public_key, self.blockchain.get_balance()))

        else:
            print('User left!')

        print('Done')


node = Node()
node.listen_user_input()