import os
import json
import random
import string


class PasswordValidator:
    @staticmethod
    def isValid(password):
        if len(password) < 8:
            return False
        hasUpper = any(c.isupper() for c in password)
        hasNumber = any(c.isdigit() for c in password)
        hasSpecial = any(c in "!@#$%^&*()" for c in password)
        return hasUpper and hasNumber and hasSpecial
class PasswordGenerator:
    @staticmethod
    def generatePassword(length=12):
        if length < 8:
            length = 8
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        while True:
            password = ''.join(random.choice(chars) for _ in range(length))
            if PasswordValidator.isValid(password):
                return password
class Account:
    def __init__(self, name, username, password, category):
        self.name = name
        self.username = username
        self.password = password
        self.category = category

    def toDict(self):
        return {
            "name": self.name,
            "username": self.username,
            "password": self.password,
            "category": self.category
        }
class FileStorage:
    dataFile = "data.json"

    @staticmethod
    def saveData(data):
        with open(FileStorage.dataFile, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def loadData():
        if not os.path.exists(FileStorage.dataFile):
            return {}
        with open(FileStorage.dataFile, "r") as f:
            return json.load(f)
class PasswordManager:
    def __init__(self, currentUser):
        self.currentUser = currentUser
        self.data = FileStorage.loadData()
        if currentUser not in self.data:
            self.data[currentUser] = []

    def save(self):
        FileStorage.saveData(self.data)

    def addAccount(self):
        name = input("Account name: ")
        username = input("Username: ")
        useGen = input("Generate secure password? (y/n): ").lower()
        if useGen == 'y':
            password = PasswordGenerator.generatePassword()
            print("Generated password:", password)
        else:
            password = input("Enter password: ")
            while not PasswordValidator.isValid(password):
                print("Password must be 8+ chars with 1 capital, 1 number, and 1 special (!@#$%^&*()).")
                password = input("Enter valid password: ")

        category = input("Category (e.g. work, games): ").lower()
        account = Account(name, username, password, category)
        self.data[self.currentUser].append(account.toDict())
        print("Account added!")

    def viewCategories(self):
        categories = set()
        for acc in self.data[self.currentUser]:
            categories.add(acc["category"])
        print("\nCategories:")
        for cat in categories:
            print("-", cat)

    def viewAccountsByCategory(self):
        category = input("Enter category: ").lower()
        found = False
        for acc in self.data[self.currentUser]:
            if acc["category"] == category:
                print(f"\nAccount: {acc['name']}")
                print(f"Username: {acc['username']}")
                print(f"Password: {acc['password']}")
                found = True
        if not found:
            print("No accounts found in that category.")

    def editAccount(self):
        name = input("Enter account name to edit: ")
        for acc in self.data[self.currentUser]:
            if acc["name"] == name:
                acc["username"] = input("New username: ")
                acc["password"] = input("New password: ")
                acc["category"] = input("New category: ").lower()
                print("Account updated.")
                return
        print("Account not found.")

    def deleteAccount(self):
        name = input("Enter account name to delete: ")
        for acc in self.data[self.currentUser]:
            if acc["name"] == name:
                self.data[self.currentUser].remove(acc)
                print("Account deleted.")
                return
        print("Account not found.")

    def run(self):
        while True:
            print("\n--- Password Manager ---")
            print("1. Add Account")
            print("2. View Categories")
            print("3. View Accounts by Category")
            print("4. Edit Account")
            print("5. Delete Account")
            print("6. Save and Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                self.addAccount()
            elif choice == '2':
                self.viewCategories()
            elif choice == '3':
                self.viewAccountsByCategory()
            elif choice == '4':
                self.editAccount()
            elif choice == '5':
                self.deleteAccount()
            elif choice == '6':
                self.save()
                print("Goodbye!")
                break
            else:
                print("Invalid choice!")
def loginSystem():
    users = {}
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            users = json.load(f)

    for i in range(3):
        print("\n--- Login ---")
        username = input("Username: ")
        if username in users:
            password = input("Password: ")
            if password == users[username]["password"]:
                print("Login successful!")
                return username
            else:
                print("Incorrect password.")
        else:
            print("User not found.")
        print(f"Attempts left: {2 - i}")
    print("Too many failed attempts. Exiting...")
    exit()

def registerUser():
    print("\n--- Register ---")
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    while not PasswordValidator.isValid(password):
        print("Password must have at least 8 chars, 1 capital, 1 number, 1 special (!@#$%^&*()).")
        password = input("Enter valid password: ")
    firstName = input("First name: ")
    lastName = input("Last name: ")

    users = {}
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            users = json.load(f)

    users[username] = {
        "password": password,
        "firstName": firstName,
        "lastName": lastName
    }

    with open("users.json", "w") as f:
        json.dump(users, f)

    print("Registration successful. Please log in.")
    return loginSystem()

def main():
    print("Welcome to the Password Manager!")
    if not os.path.exists("users.json") or input("Are you a new user? (y/n): ").lower() == 'y':
        currentUser = registerUser()
    else:
        currentUser = loginSystem()

    manager = PasswordManager(currentUser)
    manager.run()

if __name__ == "__main__":
    main()
