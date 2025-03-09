import json
import os
import hashlib
import base64
from cryptography.fernet import Fernet

DATA_FILE = 'passwords.json'

class PasswordManager:
    def __init__(self, seed):
        self.key = base64.urlsafe_b64encode(hashlib.sha256(seed.encode()).digest()).decode()
        self.passwords = self.load_password()

    def load_password(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    def add_password(self, application, user, password):
        if application not in self.passwords:
            self.passwords[application] = []
        d = {}
        d["username"] = user
        d["password"] = password
        self.passwords[application].append(d)

        with open(DATA_FILE, 'w') as f:
            json.dump(self.passwords, f, indent=4)
        return
    
    def get_password(self, application, user):
        if application not in self.passwords:
            print(f"No password for {application} is saved")
            return
        for object in self.passwords[application]:
            if object["username"] == user:
                print(f"Username: {object["username"]} \nPassword: {object["password"]}")
                return
        else:
            print(f"No passwords for {user} has been saved in {application}")
            return
    
    def update_password(self, application, user, newpassword):
        if application not in self.passwords:
            print(f"No passwords have been saved for {application}")
            return
        for index in range(len(self.passwords[application])):
            if self.passwords[application][index]["username"] == user:
                self.passwords[application][index]["password"] = newpassword
                print("\nPassword updated successfully!!\n")
                break
        else:
            print(f"No password for {user} has been saved in {application}")

        with open(DATA_FILE, 'w') as f:
            json.dump(self.passwords, f, indent=4)
        return

    
pm = PasswordManager("arjun")
print(pm.key)



# d = {
#     "instagram": [
#         {
#             "username": "arjunsharmahehe",
#             "password": "arjunwwe6969"
#         },
#         {
#             "username": "anushka",
#             "password": "btch"
#         }
#     ]
# }

# with open(DATA_FILE, 'r+') as f:
#     data = json.dump(d, f, indent=4)