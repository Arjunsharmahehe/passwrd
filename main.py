#!/usr/bin/env python3

import json
import os
import sys
import argparse
import hashlib
import base64
from cryptography.fernet import Fernet
import pyperclip as clip
from colorama import Fore

DATA_FILE = 'passwords.json'

class PasswordManager:
    def __init__(self, seed):
        self.key = base64.urlsafe_b64encode(hashlib.sha256(seed.encode()).digest()).decode()
        self.fernet = Fernet(self.key)
        self.passwords = self.load_password()

    def load_password(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    def add_password(self, application, user, password):
        if application not in self.passwords:
            self.passwords[application] = []

        for i in self.passwords[application]:
            if i["username"] == user:
                print(Fore.RED + "\nUSER PASSWORD ALREADY EXISTS\n" + Fore.WHITE)
                return

        d = {}
        d["username"] = user
        d["password"] = self.encrypt(password)
        self.passwords[application].append(d)

        with open(DATA_FILE, 'w') as f:
            json.dump(self.passwords, f, indent=4)
            print(Fore.GREEN + "\nPASSWORD STORED SUCCESSFULLY!!\n" + Fore.WHITE)
        return
    
    def get_password(self, application, user):
        try:
            if application not in self.passwords:
                print(Fore.REd + f"\nNo password for {application} is saved\n" + Fore.WHITE)
                return
            for object in self.passwords[application]:
                if object["username"] == user:
                    print(f"\nUsername: {object["username"]} \nPassword: {Fore.GREEN + self.decrypt(object["password"]) + Fore.WHITE}")
                    clip.copy(self.decrypt(object["password"]))
                    print(Fore.GREEN + "\nPassword copied to clipboard\n" + Fore.WHITE)
                    return
            else:
                print(Fore.YELLOW + f"\nNo passwords for {user} has been saved in {application}\n" + Fore.WHITE)
                return
        except:
            print(Fore.RED + "\nAN ERROR OCCURED :/ \nYou might have entered the wrong key" + Fore.WHITE)
    
    def update_password(self, application, user, newpassword):
        if application not in self.passwords:
            print(Fore.RED + f"\nNo passwords have been saved for {application}\n" + Fore.WHITE)
            return
        for index in range(len(self.passwords[application])):
            if self.passwords[application][index]["username"] == user:
                self.passwords[application][index]["password"] = self.encrypt(newpassword)
                print(Fore.GREEN + "\nPassword updated successfully!!\n" + Fore.WHITE)
                break
        else:
            print(Fore.YELLOW + f"\nNo password for {user} has been saved in {application}\n" + Fore.WHITE)

        with open(DATA_FILE, 'w') as f:
            json.dump(self.passwords, f, indent=4)
        return
    
    def list_sites(self):
        if not self.passwords:
            print(Fore.YELLOW + "\nThere is no record\n" + Fore.WHITE)
        for i in self.passwords.keys():
            print(i)

    def list_users(self, application):
        if application not in self.passwords:
            print(Fore.YELLOW + f"\nNo passwords saved for {application}\n") + Fore.WHITE
            return
        for i in self.passwords[application]:
            print(i["username"])

    def encrypt(self, plaintext):
        return self.fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, encrypted_text):
        return self.fernet.decrypt(encrypted_text.encode()).decode()
    
def main(manager):
    
    while True:
        print("\nOptions:")
        print("1) Add Password")
        print("2) Get Password")
        print("3) Update Password")
        print("4) List Stored Sites")
        print("5) List stored users")
        print("6) Exit")
        choice = input("Choose an option: ")
        print()
        
        if choice == "1":
            site = input("Enter site name: ").lower().strip()
            user = input("Enter the username/email: ").lower().strip()
            password = input("Enter password: ")
            renter_password = input("Re-enter the password: ")
            if password != renter_password:
                print(Fore.RED + "The passwords don't match :/ \nTry again...\n" + Fore.WHITE)
            else:
                manager.add_password(site, user, password)
            
        elif choice == "2":
            site = input("Enter site name: ").lower().strip()
            user = input("Enter the username/email: ").lower().strip()
            manager.get_password(site, user)
        elif choice == "3":
            site = input("Enter site name: ").lower().strip()
            user = input("Enter the username/email: ").lower().strip()
            newpassword = input("Enter the new password: ")
            renter_password = input("Re-enter the password: ")
            if newpassword != renter_password:
                print(Fore.RED + "The passwords don't match :/ \nTry again...\n" + Fore.WHITE)
            else:
                manager.update_password(site, user, newpassword)
        elif choice == "4":
            manager.list_sites()
        elif choice == "5":
            site = input("Enter site name: ").lower().strip()
            manager.list_users(site)
        elif choice == "6":
            print("Exiting password manager.")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Fore.WHITE)


if __name__ == "__main__" and getattr(sys, 'frozen', False):
    parser = argparse.ArgumentParser(description="Simple CLI Password Manager")
    parser.add_argument("action", choices=["add", "get", "list", "list-user", "init"], help="Action to perform")
    parser.add_argument("--site", help="Website name")
    parser.add_argument("--user", help="Account name")
    parser.add_argument("--password", help="Password (required for adding)")
    parser.add_argument("--seed", required=True, help="Seed for encryption")

    args = parser.parse_args()
    manager = PasswordManager(args.seed)

    if args.action == "add":
        if not args.site or not args.password or not args.user:
            site = input("Enter site name: ").lower().strip()
            user = input("Enter the username/email: ").lower().strip()
            password = input("Enter password: ")
            renter_password = input("Re-enter the password: ")
            if password != renter_password:
                print("The passwords don't match :/ \nTry again...\n")
            else:
                manager.add_password(site, user, password)
        else:
            manager.add_password(args.site, args.user, args.password)
        
    elif args.action == "get":
        if not args.site or not args.user:
            site = input("Enter site name: ").lower().strip()
            user = input("Enter the username/email: ").lower().strip()
            manager.get_password(site, user)
        else:
            manager.get_password(args.site, args.user)
        
    elif args.action == "list":
        manager.list_sites()
    elif args.action == "list-user":
        site = input("Enter site name: ")
        manager.list_users(site)
    elif args.action == "init":
        main(manager)