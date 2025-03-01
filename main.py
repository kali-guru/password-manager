from cryptography.fernet import Fernet, InvalidToken
import json
import os

# Generate a key and save it
KEY_FILE = "key.key"
DATA_FILE = "passwords.json"


def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key


key = load_key()
cipher_suite = Fernet(key)

# Load passwords
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "rb") as file:
        encrypted_data = file.read()
        try:
            decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
            passwords = json.loads(decrypted_data)
        except InvalidToken:
            print("Error: The data in the file is not valid or has been corrupted.")
            passwords = {}
else:
    passwords = {}


def save_passwords():
    encrypted_data = cipher_suite.encrypt(json.dumps(passwords).encode())
    with open(DATA_FILE, "wb") as file:
        file.write(encrypted_data)


def add_password(account, password):
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()
    passwords[account] = encrypted_password
    save_passwords()
    print(f"Password for {account} saved successfully.")


def retrieve_password(account):
    if account in passwords:
        decrypted_password = cipher_suite.decrypt(passwords[account].encode()).decode()
        print(f"Password for {account}: {decrypted_password}")
    else:
        print("Account not found.")


def update_password(account, new_password):
    if account in passwords:
        encrypted_password = cipher_suite.encrypt(new_password.encode()).decode()
        passwords[account] = encrypted_password
        save_passwords()
        print(f"Password for {account} updated successfully.")
    else:
        print("Account not found.")


def delete_password(account):
    if account in passwords:
        del passwords[account]
        save_passwords()
        print(f"Password for {account} deleted successfully.")
    else:
        print("Account not found.")


def main():
    while True:
        print("\nPassword Manager")
        print("1. Add Password")
        print("2. Retrieve Password")
        print("3. Update Password")
        print("4. Delete Password")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            account = input("Enter account name: ")
            password = input("Enter password: ")
            add_password(account, password)
        elif choice == "2":
            account = input("Enter account name: ")
            retrieve_password(account)
        elif choice == "3":
            account = input("Enter account name: ")
            new_password = input("Enter new password: ")
            update_password(account, new_password)
        elif choice == "4":
            account = input("Enter account name: ")
            delete_password(account)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
