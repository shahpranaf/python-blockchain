# import inbult library
import functools
import json

# import other classes
from block import Block
from transaction import Transaction
from utility.verification import Verification
from utility.hash_util import hash_block
from wallet import Wallet

# The reward we give to the miners for creating new block
MINING_REWARD = 10

class Blockchain:

    def __init__(self, hosting_node_id):
        genesis_block = Block(0, '', [], 100, 0)
        self.chain = [genesis_block]
        self.__open_transactions = []

        self.hosting_node_id = hosting_node_id

        self.load_data()

    
    #Getter
    @property
    def chain(self):
        return self.__chain[:]

    
    #setter
    @chain.setter
    def chain(self, val):
        self.__chain = val


    def get_chain(self):
        return self.__chain[:]

    
    def get_open_transactions(self):
        return self.__open_transactions[:]

    
    def load_data(self):

        try:
            with open('blockchain.txt', mode='r') as file:
                content = file.readlines()

                blockchain = json.loads(content[0][:-1])

                updated_blockchain = []

                for block in blockchain:
                    converted_tx = [
                        Transaction(
                            tx['sender'],
                            tx['recipient'],
                            tx['signature'],
                            tx['amount']) for tx in block['transactions']]

                    updated_block = Block(block['index'], block['previous_hash'],
                                        converted_tx, block['proof'],
                                        block['timestamp'])

                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain

                open_transactions = json.loads(content[1])
                updated_open_transactions = []

                for transaction in open_transactions:
                    updated_transaction = Transaction(transaction['sender'],
                                                    transaction['recipient'],
                                                    transaction['signature'],
                                                    transaction['amount'])

                    updated_open_transactions.append(updated_transaction)
                self.__open_transactions = updated_open_transactions

        except (IOError, IndexError):
            print("Handled Exception!!!")

        finally:
            print('Cleanup!')
    
    
    def save_data(self):

        try:
            with open('blockchain.txt', mode='w') as file:
                saveable_chain = [
                    block.__dict__ for block in [
                        Block(
                            block_el.index,
                            block_el.previous_hash,
                            [
                                tx.__dict__ for tx in block_el.transactions],
                            block_el.proof,
                            block_el.timestamp) for block_el in self.__chain]]
                file.write(json.dumps(saveable_chain))
                file.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                file.write(json.dumps(saveable_tx))
        except IOError:
            print("Error Saving File!!")


    def proof_of_work(self):

        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0

        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1

        return proof


    def get_balance(self):

        participant = self.hosting_node_id

        tx_sender = [[tx.amount for tx in block.transactions
                    if tx.sender == participant] for block in self.__chain]

        open_tx_sender = [
            tx.amount for tx in self.__open_transactions if tx.sender == participant]

        tx_sender.append(open_tx_sender)

        amt_sent = functools.reduce(
            lambda tx_sum,
            tx_amt: tx_sum +
            sum(tx_amt) if len(tx_amt) > 0 else tx_sum +
            0,
            tx_sender,
            0)

        # amt_sent = 0
        # for tx in tx_sender:
        #     if len(tx) > 0:
        #         amt_sent += tx[0]

        tx_recipeint = [[tx.amount for tx in block.transactions
                        if tx.recipient == participant] for block in self.__chain]

        amt_received = functools.reduce(
            lambda tx_sum,
            tx_amt: tx_sum +
            sum(tx_amt) if len(tx_amt) > 0 else tx_sum +
            0,
            tx_recipeint,
            0)

        # amt_received = 0
        # for tx in tx_recipeint:
        #     if len(tx) > 0:
        #         amt_received += tx[0]

        return amt_received - amt_sent


    def get_last_blockchain_value(self):
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]


    def add_transaction(self, recipient, sender, signature, amount=1.0):

        # transaction = {
        #     'sender': sender,
        #     'recipient': recipient,
        #     'amount': amount
        # }

        if self.hosting_node_id == None:
            return False

        transaction = Transaction(sender, recipient, signature, amount)

        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            # participants.add(sender)
            # participants.add(recipient)
            self.save_data()
            return True

        return False


    def mine_block(self):

        if self.hosting_node_id == None:
            return False

        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)

        proof = self.proof_of_work()

        # reward_transaction = {
        #     'sender': 'MINING',
        #     'recipient': owner,
        #     'amount': MINING_REWARD
        # }

        reward_transaction = Transaction('MINING', self.hosting_node_id, '', MINING_REWARD)

        # for key in last_block:
        #     value = last_block[key]
        #     hashed_block = hashed_block + str(value)

        # print(hashed_block)

        copied_transactions = self.__open_transactions[:]
        
        for tx in copied_transactions:
            if not Wallet.verify_transactions(tx):
                return False

        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)

    

        self.__chain.append(block)

        # Reset Open Transaction
        self.__open_transactions = []
        self.save_data()

        return True
