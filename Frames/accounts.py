import tkinter as tk
import tkinter.ttk as ttk
import mal
import json
import requests
import bcrypt

class Accounts(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.options = {'padx': 5, 'pady': 5}
        self.container = container
        self.title = ttk.Label(self, text="Accounts")
        self.title.pack(**self.options)

        self.accounts = json.load(open("animelist.json"))["Accounts"]
        self.account = tk.StringVar()

        self.account_box = ttk.Combobox(self, textvariable=self.account, values=[i["Name"] for i in self.accounts] + ["Create New Account", "Link to MAL"], state="readonly")
        self.account_box.bind("<<ComboboxSelected>>", self.set_account)
        self.account.set("Select an account")
        self.account_box.pack(**self.options)

    def set_account(self, event):
        #delete AccountForm if it exists
        #create AccountForm
        if any(i.startswith("!accountform") for i in self.children):
            for i in self.children.copy():
                if i.startswith("!accountform"):
                    self.children[i].destroy()
        self.accountform = self.AccountForm(self)
        self.accountform.pack(**self.options)

    def map_account_to_id(self, name):
        return [i for i in self.accounts if i["Name"] == name][0]["ID"]
    
    class AccountForm(ttk.Frame):
        def __init__(self, container):
            super().__init__(container)
            options = {'padx': 5, 'pady': 5}
            self.container = container
            if self.container.account.get() == "Create New Account":
                self.name = ttk.Label(self, text="Name")
                self.name.pack(**options)
                self.name_entry = ttk.Entry(self)
                self.name_entry.pack(**options)
                self.password = ttk.Label(self, text="Password")
                self.password.pack(**options)
                self.password_entry = ttk.Entry(self, show="*")
                self.password_entry.pack(**options)
                self.submit = ttk.Button(self, text="Submit", command=self.submit_button)
                self.submit.pack(**options)
            elif self.container.account.get() == "Link to MAL":
                code_verifier = code_challenge = get_new_code_verifier()
                auth_url = print_new_authorisation_url(code_challenge)

                auth_url_button = ttk.Button(self, text="Authorize", command=lambda: webbrowser.open(auth_url))
                auth_url_button.pack()

                authorisation_code = ttk.Entry(self)
                authorisation_code.pack()

                auth_code = ""

                def get_code():
                    auth_code = authorisation_code.get()

                    self.token = generate_new_token(auth_code, code_verifier)

                    user_info = requests.get("https://api.myanimelist.net/v2/users/@me", headers={"Authorization": f"Bearer {self.token['access_token']}"}).json()
                    new_account = {
                        "Name": user_info["name"],
                        "Password": None,
                        "ID": len(json.load(open("animelist.json"))["Accounts"]),
                        "linked": self.token,
                        "List": requests.get("https://api.myanimelist.net/v2/users/@me/animelist", headers={"Authorization": f"Bearer {self.token['access_token']}"}).json()
                    }
                    json.dump({"Accounts": json.load(open("animelist.json"))["Accounts"] + [new_account]}, open("animelist.json", "w"), indent=4)
                        

                submit = ttk.Button(self, text="Submit", command=get_code)
                submit.pack()



            else:
                self.name = ttk.Label(self, text=self.container.accounts[self.container.map_account_to_id(self.container.account.get())]['Name'])
                self.name.pack(**options)

                self.container.container.account = [i for i in self.container.accounts if i["Name"] == self.container.account.get()][0]["ID"]

                self.container.container.children["!listframe"].load()
        def submit_button(self):
            #create new account
            #add to json
            #set account to new account\

            new_account = {
                "Name": self.name_entry.get(),
                "Password": get_hashed_password(self.password_entry.get()).decode('utf-8'),
                "ID": len(json.load(open("animelist.json"))["Accounts"]),
                "linked": None,
                "List": []
            }

            accounts = json.load(open("animelist.json"))["Accounts"]
            accounts.append(new_account)
            json.dump({"Accounts": accounts}, open("animelist.json", "w"), indent=4)

def get_hashed_password(plain_text_password):
    plain_text_password = plain_text_password.encode('utf-8')
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    plain_text_password = plain_text_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password, hashed_password)


import secrets
import webbrowser
import time

CLIENT_ID = '4c8635f3ce144c1c7f0c83f10fb98a4c'
CLIENT_SECRET = "ff914e5548fa67ec17615d13c328b9c24818243b91778a8ac8a07a4674ecd5bd"


# 1. Generate a new Code Verifier / Code Challenge.
def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]


# 2. Print the URL needed to authorise your application.
def print_new_authorisation_url(code_challenge: str):
    global CLIENT_ID

    url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={CLIENT_ID}&code_challenge={code_challenge}'
    return url


# 3. Once you've authorised your application, you will be redirected to the webpage you've
#    specified in the API panel. The URL will contain a parameter named "code" (the Authorisation
#    Code). You need to feed that code to the application.
def generate_new_token(authorisation_code: str, code_verifier: str) -> dict:
    global CLIENT_ID, CLIENT_SECRET

    url = 'https://myanimelist.net/v1/oauth2/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': authorisation_code,
        'code_verifier': code_verifier,
        'grant_type': 'authorization_code'
    }

    response = requests.post(url, data)
    response.raise_for_status()  # Check whether the request contains errors

    token = response.json()
    response.close()

    return token