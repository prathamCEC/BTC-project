import hashlib
import time


class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = (
            str(self.index) +
            str(self.timestamp) +
            str(self.data) +
            str(self.previous_hash) +
            str(self.nonce)
        )
        return hashlib.sha256(content.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"  Block mined! Nonce: {self.nonce} | Hash: {self.hash}")


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        index = len(self.chain)
        previous_hash = self.get_latest_block().hash
        new_block = Block(index, data, previous_hash)
        print(f"\n  Mining block {index}...")
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def print_chain(self):
        print("\n" + "=" * 55)
        for block in self.chain:
            print(f"  Index        : {block.index}")
            print(f"  Timestamp    : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp))}")
            print(f"  Data         : {block.data}")
            print(f"  Previous Hash: {block.previous_hash}")
            print(f"  Hash         : {block.hash}")
            print("-" * 55)
        print("=" * 55)
