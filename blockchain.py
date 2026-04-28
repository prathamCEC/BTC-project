import hashlib
import time
import json
import os
from datetime import datetime, timezone


CHAIN_FILE = "chain.json"


class Block:
    def __init__(self, index, data, previous_hash, timestamp=None, nonce=0, hash=None):
        self.index = index
        self.timestamp = timestamp if timestamp else time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = hash if hash else self.calculate_hash()

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

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }

    @staticmethod
    def from_dict(d):
        return Block(d["index"], d["data"], d["previous_hash"], d["timestamp"], d["nonce"], d["hash"])


class Blockchain:
    def __init__(self):
        self.difficulty = 2
        if os.path.exists(CHAIN_FILE):
            self.chain = self.load_chain()
            print("  Existing blockchain loaded from disk.")
        else:
            self.chain = [self.create_genesis_block()]
            self.save_chain()
            print("  Genesis Block created for the first time.")

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
        self.save_chain()

    def save_chain(self):
        with open(CHAIN_FILE, "w") as f:
            json.dump([block.to_dict() for block in self.chain], f, indent=4)

    def load_chain(self):
        with open(CHAIN_FILE, "r") as f:
            return [Block.from_dict(d) for d in json.load(f)]

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
            dt = datetime.fromtimestamp(block.timestamp, tz=timezone.utc)
            print(f"  Index        : {block.index}")
            print(f"  Timestamp    : {dt.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            print(f"  Data         : {block.data}")
            print(f"  Previous Hash: {block.previous_hash}")
            print(f"  Hash         : {block.hash}")
            print("-" * 55)
        print("=" * 55)
