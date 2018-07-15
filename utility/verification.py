from utility.hash_util import hash_string_256, hash_block
from wallet import Wallet


class Verification:

    @staticmethod
    def valid_proof(transactions, last_hash, proof):

        guess = (str([tx.to_ordered_dict() for tx in transactions])
                 + str(last_hash) + str(proof)).encode()

        guess_hash = hash_string_256(guess)
        return guess_hash[0:2] == '00'

    @classmethod
    def verify_chain(self, blockchain):
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
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False

            if not self.valid_proof(block.transactions[:-1],
                                    block.previous_hash, block.proof):
                print("Invalid proof")
                return False

        return True


    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds=True):

        if check_funds:
            sender_balance = get_balance()
            return sender_balance >= transaction.amount and Wallet.verify_transactions(transaction)
        else:
            return Wallet.verify_transactions(transaction)


    @classmethod
    def verify_transactions(self, get_balance, open_transactions):
        return all([self.verify_transaction(tx, get_balance, False)
                    for tx in open_transactions])
