import hashlib
import json
import time

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_content = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }
        block_string = json.dumps(block_content, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, {"msg": "Genesis Block"}, "0")
        self.chain.append(genesis_block)

    def add_block(self, data):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), data, last_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.compute_hash():
                print(f"❌ Block {i} hash mismatch!")
                return False
            if current.previous_hash != previous.hash:
                print(f"❌ Block {i} not linked to previous block!")
                return False

        return True

    def save_to_file(self, filename="civ_chain.json"):
        chain_data = []
        for block in self.chain:
            block_data = {
                "index": block.index,
                "timestamp": block.timestamp,
                "data": block.data,
                "previous_hash": block.previous_hash,
                "hash": block.hash
            }
            chain_data.append(block_data)

        with open(filename, "w") as f:
            json.dump(chain_data, f, indent=4)

    def load_from_file(self, filename="civ_chain.json"):
        try:
            with open(filename, "r") as f:
                loaded_chain = json.load(f)
                self.chain = []
                for block_data in loaded_chain:
                    block = Block(
                        index=block_data["index"],
                        data=block_data["data"],
                        previous_hash=block_data["previous_hash"]
                    )
                    block.timestamp = block_data["timestamp"]
                    block.hash = block_data["hash"]
                    self.chain.append(block)
        except FileNotFoundError:
            print("⚠️ No previous chain file found. Starting fresh.")
