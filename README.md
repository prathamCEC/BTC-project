# 🔗 Python Blockchain Project

A beginner-friendly, CLI-based blockchain implementation in Python that follows the textbook definition of a blockchain — genesis block created only once, chain persisted across sessions, proof-of-work mining, and tamper detection.

---

## 📁 File Structure

```
BTC-project/
├── blockchain.py       # Core blockchain logic (Block and Blockchain classes)
├── main.py             # CLI interface and menu-driven interaction
├── chain.json          # Persistent storage of the blockchain (auto-generated at runtime)
├── requirements.txt    # Project dependencies
└── .gitignore          # Files ignored by Git
```

---

## ⚙️ How the Project Works

1. When you run `main.py`, the program checks if `chain.json` exists on disk.
2. If `chain.json` does **not** exist → Genesis Block is created **for the first time** and saved to disk.
3. If `chain.json` **exists** → the entire chain is loaded from disk, preserving all previous blocks.
4. You interact with the blockchain via a terminal menu — add transactions, view blocks, validate the chain, or tamper with a block for demonstration.
5. Every time a new block is added, the chain is automatically saved to `chain.json`.
6. When you exit and rerun the program, the chain continues from where it left off — exactly like a real blockchain network.

---

## 🚀 How to Run

```bash
cd "c:\Users\Pratham\OneDrive\Desktop\BTC-project"
python main.py
```

---

## 🖥️ CLI Menu Options

```
===================================
       BLOCKCHAIN CLI MENU
===================================
  1. Add Transaction
  2. View Blockchain
  3. Validate Blockchain
  4. Tamper with a Block
  5. Exit
===================================
```

| Option | Description |
|--------|-------------|
| 1 | Prompts for transaction data, mines a new block, and saves the chain |
| 2 | Prints all blocks with index, timestamp, data, hashes |
| 3 | Validates the entire chain for tampering or corruption |
| 4 | Tampers with a block's data to demonstrate immutability |
| 5 | Exits the program |

---

## 📦 Dependencies

This project uses **only built-in Python libraries** — no external packages required.

| Library | Purpose |
|---------|---------|
| `hashlib` | SHA-256 hashing for block hash calculation |
| `time` | Capturing block creation timestamp |
| `json` | Serializing and saving the blockchain to disk |
| `os` | Checking if `chain.json` exists on disk |
| `datetime` | Timezone-aware timestamp formatting for display |

---

## 🧠 Codebase Explanation

### `blockchain.py`

This file contains all the core blockchain logic split into two classes — `Block` and `Blockchain`.

---

#### Class: `Block`

Represents a single block in the blockchain.

---

##### `__init__(self, index, data, previous_hash, timestamp=None, nonce=0, hash=None)`

Constructor that initializes a block.

| Parameter | Description |
|-----------|-------------|
| `index` | Position of the block in the chain |
| `data` | Transaction data stored in the block |
| `previous_hash` | Hash of the previous block — links the chain |
| `timestamp` | Time of block creation. If not provided, uses current time |
| `nonce` | Number used in proof-of-work mining. Defaults to `0` |
| `hash` | If loading from disk, the saved hash is passed in. Otherwise calculated fresh |

- If `timestamp` is not provided (new block), it captures the current time using `time.time()`
- If `hash` is not provided (new block), it calls `calculate_hash()` to compute it

---

##### `calculate_hash(self)`

Computes the SHA-256 hash of the block by combining all its fields.

- Concatenates `index + timestamp + data + previous_hash + nonce` into a single string
- Encodes it and runs it through `hashlib.sha256()`
- Returns the resulting hexadecimal hash string
- This hash uniquely identifies the block — any change in data produces a completely different hash

---

##### `mine_block(self, difficulty)`

Implements **Proof-of-Work** mining.

- `difficulty` defines how many leading zeros the hash must start with (e.g., difficulty `2` means hash must start with `00`)
- Keeps incrementing `nonce` and recalculating the hash until the hash starts with the required number of zeros
- Once found, prints the nonce and final valid hash
- This makes adding a block computationally expensive, preventing easy tampering

---

##### `to_dict(self)`

Converts the block object into a Python dictionary for JSON serialization.

- Returns a dict with all block fields: `index`, `timestamp`, `data`, `previous_hash`, `nonce`, `hash`
- Used by `save_chain()` to write the block to `chain.json`

---

##### `from_dict(d)` *(static method)*

Reconstructs a `Block` object from a dictionary loaded from `chain.json`.

- Takes a dictionary `d` and passes all fields into the `Block` constructor
- Since `timestamp`, `nonce`, and `hash` are passed in, the block is restored exactly as it was — no recalculation
- Used by `load_chain()` when reading from disk

---

#### Class: `Blockchain`

Manages the full chain of blocks, persistence, validation, and display.

---

##### `__init__(self)`

Constructor that initializes the blockchain.

- Sets `difficulty = 2` (hash must start with `00`)
- Checks if `chain.json` exists on disk using `os.path.exists()`
  - If **yes** → calls `load_chain()` to restore the existing chain
  - If **no** → calls `create_genesis_block()` to create the genesis block, then `save_chain()` to persist it
- This ensures the genesis block is created **only once**, ever

---

##### `create_genesis_block(self)`

Creates the very first block in the blockchain — the Genesis Block.

- Creates a `Block` with index `0`, data `"Genesis Block"`, and previous hash `"0"` (no previous block)
- Called only when `chain.json` does not exist

---

##### `get_latest_block(self)`

Returns the last block in the chain.

- Used by `add_block()` to get the hash of the current last block, which becomes the `previous_hash` of the new block

---

##### `add_block(self, data)`

Creates, mines, and appends a new block to the chain.

- Automatically assigns the index as `len(self.chain)`
- Gets `previous_hash` from the latest block using `get_latest_block()`
- Creates a new `Block` object with the transaction data
- Calls `mine_block()` to perform proof-of-work
- Appends the mined block to `self.chain`
- Calls `save_chain()` to persist the updated chain to disk immediately

---

##### `save_chain(self)`

Saves the entire blockchain to `chain.json`.

- Converts each block to a dictionary using `to_dict()`
- Writes the list of dictionaries to `chain.json` using `json.dump()` with indentation for readability

---

##### `load_chain(self)`

Loads the blockchain from `chain.json` and reconstructs it in memory.

- Reads `chain.json` using `json.load()`
- Converts each dictionary back into a `Block` object using `Block.from_dict()`
- Returns the reconstructed list of blocks

---

##### `is_chain_valid(self)`

Validates the integrity of the entire blockchain.

- Loops through every block starting from index `1` (skips genesis block)
- For each block, checks two things:
  1. `current.hash == current.calculate_hash()` — verifies the stored hash matches a fresh recalculation. If data was tampered, this will fail
  2. `current.previous_hash == previous.hash` — verifies the chain linkage is intact
- Returns `True` if all checks pass, `False` if any block has been tampered with

---

##### `print_chain(self)`

Prints all blocks in a clean formatted layout.

- Loops through every block in the chain
- Converts the raw `timestamp` (Unix float) to a human-readable UTC string using `datetime.fromtimestamp()` with `tz=timezone.utc`
- Prints `index`, `timestamp`, `data`, `previous_hash`, and `hash` for each block
- Uses separators for clean visual output

---

### `main.py`

Entry point of the application. Handles the CLI menu and user interaction.

---

##### `print_menu()`

Prints the CLI menu to the terminal.

- Displays all 5 options in a formatted box
- Called at the start of every loop iteration so the menu is always visible

---

##### `main()`

Main function that runs the interactive loop.

- Creates a `Blockchain()` instance — this either loads from disk or creates the genesis block
- Runs an infinite `while True` loop showing the menu and reading user input
- Validates input — if choice is not `1-5`, prints an error and loops again
- **Option 1** — reads transaction data, validates it's not empty, calls `add_block()`
- **Option 2** — calls `print_chain()` to display all blocks
- **Option 3** — calls `is_chain_valid()` and prints `VALID ✓` or `INVALID ✗`
- **Option 4** — takes a block index and fake data from user, directly modifies `block.data` in memory without updating the hash — this breaks the chain integrity intentionally for demonstration
- **Option 5** — breaks the loop and exits the program

---

## 🔐 Key Blockchain Concepts Demonstrated

| Concept | How it's implemented |
|--------|----------------------|
| Genesis Block | Created only once when `chain.json` doesn't exist |
| Chain Linking | Each block stores the hash of the previous block |
| Proof-of-Work | `mine_block()` increments nonce until hash meets difficulty target |
| Immutability | Tampering with data changes the hash, breaking `is_chain_valid()` |
| Persistence | Chain saved to `chain.json` and reloaded on every run |
| SHA-256 Hashing | Every block's identity is a SHA-256 hash of its contents |

---

## 🧪 Demo Guide (For Presentation)

1. Delete `chain.json` if it exists to start fresh
2. Run `python main.py` → see `Genesis Block created for the first time.`
3. Add 2-3 transactions using option `1`
4. View the chain using option `2` — observe how each block's `Previous Hash` matches the previous block's `Hash`
5. Validate using option `3` → `VALID ✓`
6. Exit with option `5`
7. Run `python main.py` again → see `Existing blockchain loaded from disk.` — genesis block not recreated
8. Use option `4` to tamper with a block
9. Validate using option `3` → `INVALID ✗` — demonstrates immutability
