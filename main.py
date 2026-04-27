from blockchain import Blockchain

def print_menu():
    print("\n" + "=" * 35)
    print("       BLOCKCHAIN CLI MENU")
    print("=" * 35)
    print("  1. Add Transaction")
    print("  2. View Blockchain")
    print("  3. Validate Blockchain")
    print("  4. Exit")
    print("=" * 35)

def main():
    my_blockchain = Blockchain()
    print("\n  Blockchain initialized with Genesis Block.")

    while True:
        print_menu()
        choice = input("  Enter your choice (1-4): ").strip()

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
            print("\n  Exiting... Goodbye!\n")
            break

        else:
            print("  Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
