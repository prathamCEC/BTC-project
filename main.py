from blockchain import Blockchain
import threading
import viewer

def print_menu():
    print("\n" + "=" * 35)
    print("       BLOCKCHAIN CLI MENU")
    print("=" * 35)
    print("  1. Add Transaction")
    print("  2. View Blockchain")
    print("  3. Validate Blockchain")
    print("  4. Tamper with a Block")
    print("  5. Launch Visual Viewer")
    print("  6. Exit")
    print("=" * 35)

def main():
    my_blockchain = Blockchain()
    print("\n  Blockchain initialized with Genesis Block.")

    while True:
        print_menu()
        choice = input("  Enter your choice (1-6): ").strip()

        if choice == "1":
            data = input("  Enter transaction data: ").strip()
            if not data:
                print("  Transaction data cannot be empty.")
                continue
            my_blockchain.add_block(data)
            print("  Block added to the blockchain!")

        elif choice == "2":
            print("\n  --- Blockchain ---")
            my_blockchain.print_chain()

        elif choice == "3":
            valid = my_blockchain.is_chain_valid()
            status = "VALID ✓" if valid else "INVALID ✗"
            print(f"\n  Blockchain status: {status}")

        elif choice == "4":
            chain_len = len(my_blockchain.chain)
            if chain_len <= 1:
                print("  No blocks to tamper with. Add a transaction first.")
                continue
            print(f"  Available block indexes: 1 to {chain_len - 1}")
            try:
                idx = int(input("  Enter block index to tamper: ").strip())
                if idx < 1 or idx >= chain_len:
                    print("  Invalid index.")
                    continue
            except ValueError:
                print("  Please enter a valid number.")
                continue
            new_data = input("  Enter fake data: ").strip()
            my_blockchain.chain[idx].data = new_data
            my_blockchain.save_chain()
            print(f"  Block {idx} tampered! Run Validate Blockchain to see the effect.")

        elif choice == "5":
            t = threading.Thread(target=viewer.launch, daemon=True)
            t.start()
            input("  Press Enter to return to menu...")

        elif choice == "6":
            print("\n  Exiting... Goodbye!\n")
            break

        else:
            print("  Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
