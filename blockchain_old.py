import functools
import hashlib as hl
from collections import OrderedDict
import json

from hash_util import hash_block, hash_string_256

MINING_REWARD = 10

genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Panna'
participants = {'Panna'}


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def save_data():

    try:
        with open('blockchain.txt', mode='w') as file:
            file.write(json.dumps(blockchain))
            file.write('\n')
            file.write(json.dumps(open_transactions))
    except IOError:
        print("Error Saving File!!")


def load_data():

    try:
        with open('blockchain.txt', mode='r') as file:
            content = file.readlines()

            global blockchain
            global open_transactions

            blockchain = json.loads(content[0][:-1])
            updated_blockchain = []

            for block in blockchain:
                updated_block = {
                    'previous_hash': block['previous_hash'],
                    'index': block['index'],
                    'transactions': [
                        OrderedDict(
                            [
                                ('sender',
                                 tx['sender']),
                                ('recipient',
                                 tx['recipient']),
                                ('amount',
                                 tx['amount'])]) for tx in block['transactions']],
                    'proof': block['proof']}
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain

            open_transactions = json.loads(content[1])
            updated_open_transactions = []

            for transaction in open_transactions:
                updated_transaction = OrderedDict([
                    ('sender', transaction['sender']),
                    ('recipient', transaction['recipient']),
                    ('amount', transaction['amount'])
                ])
                updated_open_transactions.append(updated_transaction)
            open_transactions = updated_open_transactions

    except IOError:
        genesis_block = {
            'previous_hash': '',
            'index': 0,
            'transactions': [],
            'proof': 100
        }
        blockchain = [genesis_block]
        open_transactions = []

    finally:
        print('Cleanup!')


load_data()


def add_transaction(recipient, sender=owner, amount=1.0):

    # transaction = {
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount
    # }

    transaction = OrderedDict([
        ('sender', sender),
        ('recipient', recipient),
        ('amount', amount)
    ])

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True

    return False


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()

    guess_hash = hash_string_256(guess)
    print(guess_hash)

    return guess_hash[0:2] == '00'


def proof_of_work():

    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0

    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1

    return proof


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions]
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

    tx_recipeint = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]

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


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    proof = proof_of_work()

    # reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD
    # }

    reward_transaction = OrderedDict([
        ('sender', 'MINING'),
        ('recipient', owner),
        ('amount', MINING_REWARD)
    ])

    # for key in last_block:
    #     value = last_block[key]
    #     hashed_block = hashed_block + str(value)

    # print(hashed_block)

    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }
    blockchain.append(block)

    return True


def get_transaction_value():
    tx_recipient = input("Enter the name of recipient: ")
    tx_amount = float(input("Please enter an amount: "))

    return tx_recipient, tx_amount


def get_user_choice():
    return input("Your choice: ")


def print_block_data():
    for block in blockchain:
        print(block)


def verify_chain():
    # block_index = 0
    # is_valid = True
    # print(blockchain)
    # for  block_index in range(len(blockchain)):

    #     if block_index == 0:
    #         block_index += 1
    #         continue
    #     elif blockchain[block_index][0] == blockchain[block_index-1]:
    #         is_valid = True
    #     else:
    #         is_valid = False
    #         break
    #     block_index += 1

    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False

        if not valid_proof(block['transactions'][:-1],
                           block['previous_hash'], block['proof']):
            print("Invalid proof")
            return False

    return True


waiting_for_input = True
while waiting_for_input:
    print('Please Choose')
    print('1. Add a new transaction value!')
    print('2. Mine the block')
    print('3. Print the block data')
    print('4. Print the participants')
    print('h. Manipulate the chain')
    print('q. Quit')
    user_choice = get_user_choice()

    if user_choice == '1':
        txn_data = get_transaction_value()
        recipient, amount = txn_data
        if add_transaction(recipient, amount=amount):
            print('Transaction Successfull')
        else:
            print('Transaction Declined')

    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            save_data()

    elif user_choice == '3':
        print_block_data()

    elif user_choice == '4':
        print(participants)

    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {'previous_hash': '', 'index': 0, 'transactions': [
                {'sender': "Panna", "recipient": "Channa", "amount": '100'}]}

    elif user_choice == 'q':
        waiting_for_input = False

    else:
        print("Input is not valid. Please select from the list!!")

    print('Balance of {}: {:6.2f}'.format('Panna', get_balance('Panna')))
    # print(blockchain)

    # print(open_transactions)

    if not verify_chain():
        print('Invalid Blockchain')
        break


print('Done')
